from django.urls import path

from . import views

urlpatterns = [
    path("", views.destination_lists, name = 'destination_lists'),
    path("<int:destination_id>/", views.destination_detail_view, name='details'),
 ]