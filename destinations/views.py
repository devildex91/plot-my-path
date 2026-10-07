from django.shortcuts import get_object_or_404, render

from .models import Attraction, Destination


# Create your views here.
def destination_lists(request):
    destination = Destination.objects.all()
    return render(request, 'destinations/destination.html', { 'destinations': destination })


def destination_detail_view(request, destination_id):
    destination = get_object_or_404(Destination, id= destination_id)

    return render(request, 'destinations/destination_detail.html', {'destination': destination})