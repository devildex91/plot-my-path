from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from formtools.wizard.views import SessionWizardView

from accounts.models import TravelPreference
from destinations.models import Attraction

from .forms import (
    DestinationWizardForm,
    PreferenceWizardForm,
    ReviewForm,
    TripDetailsWizardForm,
)
from .models import Trip, TripDay

FORMS = [
    ("preferences", PreferenceWizardForm),
    ("destination", DestinationWizardForm),
    ("details", TripDetailsWizardForm),
    ("review", ReviewForm),
]


class CreateTripView(LoginRequiredMixin, SessionWizardView):
    form_list = FORMS
    template_name = "trips/trips.html"

    def done(self, form_list, **kwargs):

        preference_form = form_list[0]
        destination_form = form_list[1]
        details_form = form_list[2]

        preference, created = TravelPreference.objects.get_or_create(
            user=self.request.user
        )

        for field, value in preference_form.cleaned_data.items():
            setattr(preference, field, value)

        preference.save()

        trip = Trip.objects.create(
            destination=destination_form.cleaned_data["destination"],
            name=destination_form.cleaned_data["name"],
            start_date=details_form.cleaned_data["start_date"],
            end_date=details_form.cleaned_data["end_date"],
            budget=details_form.cleaned_data["budget"],
            status=details_form.cleaned_data["status"],
            user=self.request.user,
        )

        return redirect("itinerary_builder", trip_id=trip.id)


@transaction.atomic
def generate_trip_days(trip):
    current_date = trip.start_date
    day_number = 1

    while current_date <= trip.end_date:
        TripDay.objects.get_or_create(
            trip=trip,
            date=current_date,
            defaults={
                "day_number": day_number,
            },
        )

        current_date += timedelta(days=1)
        day_number += 1

    return trip.trip_days.order_by("day_number")


@login_required
def itinerary_builder(request, trip_id):

    trip_instance = get_object_or_404(
        Trip.objects.select_related("destination"),
        id=trip_id,
        user=request.user,
    )
    destination_attractions = Attraction.objects.filter(destination=trip_instance.destination)
    
    attractions_data = [
        {
            "id": attraction.id,
            "name": attraction.name,
            "description": attraction.description,
            "image_url": attraction.get_image_url,
        }
        for attraction in destination_attractions
    ]
    trip_days = generate_trip_days(trip_instance)
    pref_instance = TravelPreference.objects.filter(user=request.user).first()

    
  

    preferences_data = None

    if pref_instance:
        preferences_data = {
            "travel_style": pref_instance.travel_style,
            "budget_level": pref_instance.budget_level,
            "walking_preference": pref_instance.walking_preference,
            "culture": pref_instance.culture,
            "food": pref_instance.food,
            "nature": pref_instance.nature,
            "history": pref_instance.history,
            "nightlife": pref_instance.nightlife,
            "family_friendly": pref_instance.family_friendly,
            "solo_travel": pref_instance.solo_travel,
            "include_weather": pref_instance.include_weather,
        }

   
    days_data = [
        {
            "id": day.id,
            "date": day.date.isoformat(),
            "day_number": day.day_number,
            "notes": day.notes,
            "activities": [
                {
                    "id": activity.id,
                    "attraction_id": activity.attraction_id,
                    "start_time": activity.start_time.isoformat(),
                    "end_time": activity.end_time.isoformat(),
                    "order": activity.order,
                    "notes": activity.notes,
                    "status": activity.status,
                }
                for activity in day.planned_activities.all().order_by("order")
            ],
        }
        for day in trip_days
    ]

    
    serialized_data = {
        "trip": {
            "id": trip_instance.id,
            "name": trip_instance.name,
            "start_date": trip_instance.start_date.isoformat(),
            "end_date": trip_instance.end_date.isoformat(),
            "budget": str(trip_instance.budget),
            "status": trip_instance.status,
            "destination": {
                "id": trip_instance.destination.id,
                "name": str(trip_instance.destination),
            },
        },
        "preferences": preferences_data,
        "days": days_data,
        "attractions": attractions_data,
    }

    return render(
        request,
        "trips/itinerary_builder.html",
        {
            "trip": trip_instance,
            "app_data": serialized_data,

        },
    )

@login_required
def my_trips(request):
    trips = (
        request.user.trips
        .select_related("destination")
        .order_by("-start_date")
    )
    return render (request,'trips/my_trips.html', {"trips": trips})
