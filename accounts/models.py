from typing import ClassVar

from django.conf import settings
from django.db import models

from destinations.models import Destination

# Create your models here.

class TravelPreference(models.Model):

    TRAVEL_STYLE_CHOICES: ClassVar[list[tuple[str, str]]] = [
    ("adventure", "Adventure"),
    ("relaxation", "Relaxation"),
    ("city_break", "City Break"),
    ("culture", "Culture"),
    ("foodie", "Food & Drink"),
    ("nature", "Nature"),
]

    BUDGET_LEVEL_CHOICES: ClassVar[list[tuple[str, str]]] = [
    ("budget", "Budget"),
    ("mid_range", "Mid Range"),
    ("luxury", "Luxury"),
]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    travel_style = models.CharField(
        max_length=50,
        choices=TRAVEL_STYLE_CHOICES
    )

    budget_level = models.CharField(
        max_length=20,
        choices=BUDGET_LEVEL_CHOICES
    )

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


    