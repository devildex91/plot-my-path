from django.urls import path

from . import views

urlpatterns = [

path("", views.CreateTripView.as_view(), name = 'organise_trip'),
path("<int:trip_id>/itinerary/", views.itinerary_builder, name="itinerary_builder",),
path("my_trips/", views.my_trips, name='my_trips', ),
 path("<int:trip_id>/days/<int:day_id>/add-activity/", views.add_activity, name="add_activity"),
 path("<int:trip_id>/itinerary/activities/<int:activity_id>/delete/", views.delete_activity, name="delete_activity"),
]