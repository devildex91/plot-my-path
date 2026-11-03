"""URL routes for checkout pages, payment results, and Stripe webhooks."""

from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
    path('stripe/webhook/', views.stripe_webhook, name= "stripe_webhook"),
    path("refund/", views.request_refund, name="request_refund"),
]