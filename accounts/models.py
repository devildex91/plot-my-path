from django.conf import settings
from django.db import models

from destinations.models import Destination

# Create your models here.

class TravelPreference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    travel_style = models.CharField(max_length=100)
    budget_level = models.CharField(max_length=50)
    walking_preference = models.BooleanField(default=False)
    culture = models.BooleanField(default=False)
    food = models.BooleanField(default=False)
    nature = models.BooleanField(default=False)
    history = models.BooleanField(default=False)
    nightlife = models.BooleanField(default=False)
    family_friendly = models.BooleanField(default=False)
    solo_travel = models.BooleanField(default=False)
    include_weather = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferences for {self.user.username}"


class SavedDestination(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_destinations')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='saved_by_users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'destination')

    def __str__(self):
        return f"{self.user.username} saved {self.destination.name}"


    