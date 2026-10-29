from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Country, Destination


# Create your views here.
@login_required
def destination_lists(request):
    """Render destinations, optionally filtered by the selected continent."""
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
        "destinations/destination.html",
        {
            "destinations": destinations,
            "selected_continent": continent,
            "continents": continents,
        },
    )


@login_required
def destination_detail_view(request, destination_id):
    """Render one destination and its related attractions."""
    destination = get_object_or_404(Destination, id=destination_id)
    attractions = destination.attractions.all()

    return render(
        request,
        "destinations/destination_detail.html",
        {"destination": destination, "attractions": attractions},
    )


def search_destinations(request):
    """Return up to ten destination matches for the frontend search box."""
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
    """Return a small random selection of destinations for the homepage."""
    destinations = Destination.objects.order_by("?")[:3]

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
