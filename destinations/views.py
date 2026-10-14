from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import random
from .models import Attraction, Destination, Country


# Create your views here.
@login_required
def destination_lists(request):

    continents = (
        Country.objects.values_list("continent", flat=True)
        .distinct()
        .order_by("continent")
    )

    continent = request.GET.get("continent", "all")

    destinations = Destination.objects.all()

    if continent != "all":
        destinations = destinations.filter(country__continent__iexact=continent)
    return render(
    request,
    'destinations/destination.html',
    {
        'destinations': destinations,
        'selected_continent': continent,
        'continents': continents,
    },
)


@login_required
def destination_detail_view(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)

    return render(
        request, "destinations/destination_detail.html", {"destination": destination}
    )


def search_destinations(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse({"results": []})

    destinations = Destination.objects.filter(name__icontains=query)[:10]

    results_data = [
        {
            "id": d.id,
            "name": d.name,
            "slug": d.slug,
            "description": d.description,
            "cost": d.average_cost_per_day,
            "image_url": d.get_image_url,
        }
        for d in destinations
    ]
    return JsonResponse({"results": results_data})


@login_required
def popular_destinations(request):
    """
    returns a random order of destinations then returns the first two to display on the main page
    """
    destinations = Destination.objects.order_by("?")[:2]

    results_data = [
        {
            "id": d.id,
            "name": d.name,
            "slug": d.slug,
            "description": d.description,
            "cost": d.average_cost_per_day,
            "image_url": d.get_image_url,
        }
        for d in destinations
    ]

    return JsonResponse({"results": results_data})


@login_required
def organise_trip(request):

    return render(request, "destinations/trips.html")
