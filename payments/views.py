from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

