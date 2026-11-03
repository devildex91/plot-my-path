# trips/permissions.py
from .models import Trip

FREE_TRIP_LIMIT = 1

def is_premium(user):
    membership = getattr(user, "membership", None)
    return bool(membership and membership.is_active)

def can_create_trip(user):
    if user.is_staff or is_premium(user):
        return True
    return Trip.objects.filter(user=user).count() < FREE_TRIP_LIMIT