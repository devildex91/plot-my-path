from django.urls import path

from . import views

urlpatterns = [

path("", views.CreateTripView.as_view(), name = 'organise_trip'),
]