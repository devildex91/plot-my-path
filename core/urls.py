from django.urls import path

from . import views

urlpatterns = [
path("", views.landing_page_view, name ='landing_page'),
path("onboarding/", views.onboarding_page_view, name = 'onboarding_page'),
path("home/", views.homepage_view, name = 'home'),

]