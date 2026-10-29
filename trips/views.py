import json
from datetime import timedelta
from json import JSONDecodeError

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.dateparse import parse_time
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods, require_POST
from formtools.wizard.views import SessionWizardView

from accounts.models import TravelPreference
from destinations.models import Attraction

from .forms import (
    DestinationWizardForm,
    PreferenceWizardForm,
    ReviewForm,
    TripDetailsWizardForm,
)
from .models import PlannedActivity, Trip, TripDay

FORMS = [
    ("preferences", PreferenceWizardForm),
    ("destination", DestinationWizardForm),
    ("details", TripDetailsWizardForm),
    ("review", ReviewForm),
]


class CreateTripView(LoginRequiredMixin, SessionWizardView):
    """Collect trip preferences and details across the multi-step creation flow."""
    form_list = FORMS
    template_name = "trips/trips.html"

    def done(self, form_list, **kwargs):
        """Save the user's preferences and trip after all wizard steps validate."""
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
    """Create any missing calendar days for a trip and return them in order.

    ``get_or_create`` makes this safe to call whenever the itinerary is opened.
    """
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
@ensure_csrf_cookie
def itinerary_builder(request, trip_id):
    """Render the owner's itinerary with serialized trip, attraction, and weather data."""
    trip_instance = get_object_or_404(
        Trip.objects.select_related("destination"),
        id=trip_id,
        user=request.user,
    )
    destination_attractions = Attraction.objects.filter(destination=trip_instance.destination)

    weather_data = []
    weather_error = None

    if not settings.WEATHER_API_KEY:
        weather_error = "Weather API key is not configured."

    elif (
        trip_instance.destination.latitude is not None
        and trip_instance.destination.longitude is not None
    ):
        try:
            weather_data = get_destination_weather(
                latitude=trip_instance.destination.latitude,
                longitude=trip_instance.destination.longitude,
                start_date=trip_instance.start_date,
                end_date=trip_instance.end_date,
        )

        except (requests.RequestException, ValueError):
            weather_error = "Trip weather is temporarily unavailable."

    else:
        weather_error = "Destination coordinates are unavailable."

    attractions_data = [
        {
            "id": attraction.id,
            "name": attraction.name,
            "description": attraction.description,
            "entry_cost": attraction.entry_cost,
            "image_url": attraction.get_image_url,
            "latitude": str(attraction.latitude),
            "longitude": str(attraction.longitude),
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
        }

   
    days_data = [
        {
            "id": day.id,
            "date": day.date.isoformat(),
            "day_number": day.day_number,
            "notes": day.notes,
            "add_activity_url": reverse(
                "add_activity",
                kwargs={"trip_id": trip_instance.id, "day_id": day.id},
            ),
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
                "latitude": str(trip_instance.destination.latitude),
                "longitude": str(trip_instance.destination.longitude),
            },
        },
        "preferences": preferences_data,
        "days": days_data,
        "attractions": attractions_data,
        "weather": weather_data,
        "weather_error": weather_error,
    }

    return render(
        request,
        "trips/itinerary_builder.html",
        {
            "trip": trip_instance,
            "app_data": serialized_data,
           

        },
    )



def get_destination_weather(latitude, longitude, start_date, end_date):
    """Fetch daily forecast data for the destination and trip date range.

    Raises request or response parsing errors so the caller can report unavailable
    weather without preventing the itinerary itself from loading.
    """
    url = (
        "https://weather.visualcrossing.com/"
        "VisualCrossingWebServices/rest/services/"
        f"timeline/{latitude},{longitude}/"
        f"{start_date.isoformat()}/{end_date.isoformat()}"
    )

    response = requests.get(
        url,
        params={
            "unitGroup": "metric",
            "key": settings.WEATHER_API_KEY,
            "contentType": "json",
            "include": "days",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return [
        {
            "date": day["datetime"],
            "tempmax": day.get("tempmax"),
            "tempmin": day.get("tempmin"),
            "conditions": day.get("conditions"),
            "precipprob": day.get("precipprob"),
            "icon": day.get("icon"),
        }
        for day in data.get("days", [])
    ]


@login_required
def my_trips(request):
    """Render the signed-in user's trips, with the most recent start date first."""
    trips = (
        request.user.trips
        .select_related("destination")
        .order_by("-start_date")
    )
    return render (request,'trips/my_trips.html', {"trips": trips})

@login_required
@require_POST
@transaction.atomic
def add_activity(request, trip_id, day_id):
    """Validate and create an attraction activity for one of the user's trip days."""
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    day = get_object_or_404(TripDay, id=day_id, trip=trip)

    if not request.body:
        return JsonResponse({"error": "Empty request body."}, status=400)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    attraction_id = data.get("attraction_id")
    start_time_value = data.get("start_time")
    end_time_value = data.get("end_time")

    if attraction_id is None or not start_time_value or not end_time_value:
        return JsonResponse(
            {"error": "Missing attraction_id, start_time, or end_time."},
            status=400,
        )

    if not isinstance(start_time_value, str) or not isinstance(end_time_value, str):
        return JsonResponse({"error": "Times must be valid ISO 8601 times."}, status=400)

    try:
        start_time = parse_time(start_time_value)
        end_time = parse_time(end_time_value)
    except ValueError:
        return JsonResponse({"error": "Times must be valid ISO 8601 times."}, status=400)

    if start_time is None or end_time is None:
        return JsonResponse({"error": "Times must be valid ISO 8601 times."}, status=400)

    attraction = get_object_or_404(
        Attraction,
        id=attraction_id,
        destination=trip.destination,
    )

    if start_time >= end_time:
        return JsonResponse({"error": "End time must be after start time."}, status=400)

    order = day.planned_activities.count() + 1
    activity = PlannedActivity.objects.create(
        trip_day=day,
        attraction=attraction,
        start_time=start_time,
        end_time=end_time,
        order=order,
        status="scheduled",
    )

    return JsonResponse(
        {
            "activity": {
                "id": activity.id,
                "attraction_id": activity.attraction_id,
                "start_time": activity.start_time.isoformat(),
                "end_time": activity.end_time.isoformat(),
                "order": activity.order,
                "notes": activity.notes,
                "status": activity.status,
            }
        },
        status=201,
    )

@login_required
@require_http_methods(["DELETE"])
@transaction.atomic
def delete_activity(request, trip_id, activity_id):
    """Delete an activity owned through the requested trip, then close order gaps."""
    activity = get_object_or_404(
        PlannedActivity.objects.select_related("trip_day__trip"),
        id=activity_id,
        trip_day__trip_id=trip_id,  # Secures the lookup context
        trip_day__trip__user=request.user
    )
    day = activity.trip_day
    activity.delete()
    
    
    remaining_activities = day.planned_activities.order_by("start_time")
    for index, remaining_activity in enumerate(remaining_activities, start=1):
        if remaining_activity.order != index:
            remaining_activity.order = index
            remaining_activity.save(update_fields=["order"])
            
    return JsonResponse({"success": True, "message": "Activity deleted successfully."})

