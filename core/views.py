from datetime import datetime

from allauth.account import app_settings
from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class CustomSignUpView(SignupView):
    def form_valid(self, form):
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
    return render(request, 'core/landing_page.html',)

def onboarding_page_view(request):
    return render(request, 'core/onboarding.html',)

@login_required
def homepage_view(request):
    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting ="Good afternoon"
    else:
        greeting = "Good evening"

    return render(request, 'core/home.html', {'greeting': greeting} )
