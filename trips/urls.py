from django.urls import path

from . import views

urlpatterns = [

path("", views.CreateTripView.as_view(), name = 'organise_trip'),
path("<int:trip_id>/itinerary/", views.itinerary_builder, name="itinerary_builder",),
path("my_trips/", views.my_trips, name='my_trips', ),
]