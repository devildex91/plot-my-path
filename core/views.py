from datetime import datetime

from allauth.account import app_settings
from allauth.account.views import SignupView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from destinations.models import Destination

from .forms import ContactForm


class CustomSignUpView(SignupView):
    def form_valid(self, form):
        """Show the appropriate confirmation after allauth accepts the signup."""
        response = super().form_valid(form)

        if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
            messages.info(
                self.request, 
                "We've sent you an email to verify your account. Please check your inbox."
            )
        else:
            messages.success(
                self.request,
                f"Welcome {form.cleaned_data['first_name']}! Your account has been created."
            )
        return response


def landing_page_view(request):
    """Render the public landing page."""
    return render(request, 'core/landing_page.html',)

def onboarding_page_view(request):
    """Render the introductory onboarding carousel."""
    return render(request, 'core/onboarding.html',)

@login_required
def homepage_view(request):
    """Show a time-appropriate greeting and a small set of featured destinations."""
    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good morning"
        icon = "fa-solid fa-mountain-sun"
    elif hour < 18:
        greeting ="Good afternoon"
        icon ="fa-solid fa-sun"
    else:
        greeting = "Good evening"
        icon = "fa-solid fa-moon"

    destinations = Destination.objects.order_by('?')[:2]

    
    context = {
        'greeting': greeting,
        'icon': icon,
        'popular_destinations': destinations
        
    }
    
    return render(request, 'core/home.html', context)

def contact(request):
    """Renders a contact form for help page"""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            EmailMessage(
                subject=f"[Contact] {data['subject']}",
                body=f"From: {data['name']} <{data['email']}>\n\n{data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[data["email"]],
            ).send()
            messages.success(request, "Thanks, your message has been sent.")
            return redirect("contact")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        form = ContactForm(initial=initial)

    return render(request, "core/contact.html", {"form": form})
