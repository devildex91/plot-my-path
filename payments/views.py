"""Views for starting Stripe Checkout and recording completed payments."""

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Payment, PremiumMembership

STRIPE_PREMIUM_PRICE_ID = settings.STRIPE_PREMIUM_PRICE_ID
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


def has_active_membership(user):
    """Return whether the user already has a membership in the active state."""
    return PremiumMembership.objects.filter(user=user, status="active").exists()


def fulfill_checkout(session):
    """Record a paid Stripe Checkout session and activate its user's membership.

    The success redirect and Stripe webhook both call this function. Looking up
    the payment by its Stripe payment ID prevents duplicate payment records;
    the transaction keeps payment and membership creation together.
    """
    user = get_user_model().objects.get(pk=session["client_reference_id"])

    with transaction.atomic():
        payment, created = Payment.objects.get_or_create(
            stripe_payment_id=session["payment_intent"],
            defaults={
                "user": user,
                "amount": session["amount_total"],
                "currency": session["currency"],
                "status": "succeeded",
            },
        )
        if created:
            PremiumMembership.objects.update_or_create(
                user=user,
                defaults={
                    "status": "active",
                    "payment": payment,
                    "started_at": timezone.now(),
                },
            )
    return user


@login_required
def checkout(request):
    """Show the checkout page unless the signed-in user is already premium."""
    if has_active_membership(request.user):
        return redirect("profile")
    return render(request, 'payments/checkout.html')


@login_required
@require_POST
def create_checkout_session(request):
    """Create a one-time Stripe Checkout session for the signed-in user."""
    if has_active_membership(request.user):
        return JsonResponse(
            {"error": "You already have an active premium membership."},
            status=409,
        )

    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price': STRIPE_PREMIUM_PRICE_ID,
                'quantity': 1,
            }],
            mode="payment",
            success_url=request.build_absolute_uri(reverse('payment_success'))
            + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('payment_failed')),
            client_reference_id=str(request.user.id),
        )
        return JsonResponse({'checkout_url': session.url})

    except stripe.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
def payment_success(request):
    """Verify the returned Checkout session before showing payment success."""
    session_id = request.GET.get("session_id")

    if not session_id:
        return JsonResponse({"error": "Missing session ID"}, status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        client_reference_id = session.client_reference_id

        if client_reference_id != str(request.user.id):
            return JsonResponse({"error": "Invalid session"}, status=403)

        if session.payment_status != "paid":
            return JsonResponse({"error": "Payment not completed"}, status=400)

        fulfill_checkout(session)

        return render(request, 'payments/success.html', {
            "customer_name": request.user.get_full_name() or request.user.username
        })

    except stripe.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)


def payment_failed(request):
    """Render the payment failure page with an optional message from the URL."""
    error_message = request.GET.get("error", "Your payment could not be processed. Please try again")

    return render(request, "payments/failed.html", {'error_message': error_message})


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Accept signed Stripe events and fulfill completed, paid Checkout sessions."""
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        if session["payment_status"] == "paid":
            try:
                fulfill_checkout(session)
            except get_user_model().DoesNotExist:
                print("Webhook: no user for", session["client_reference_id"])

    return JsonResponse({"status": "success"}, status=200)
