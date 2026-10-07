from django.http import HttpResponse
from django.shortcuts import render


def landing_page_view(request):
    return render(request, 'core/landing_page.html',)

def homepage_view(request):
    return render(request, 'core/home.html',)

def onboarding_page_view(request):
    return render(request, 'core/onboarding.html',)