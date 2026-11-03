from django.urls import path

from . import views

urlpatterns = [
    path("", views.profile_page, name="profile",),
    path("favourite_destinations/", views.favourite_destinations, name="favourite_destinations"),
    path( "favourites/destination/<int:destination_id>/",
    views.toggle_destination_favourite,
    name="toggle_destination_favourite",
),
    
 ]