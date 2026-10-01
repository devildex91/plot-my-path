from typing import ClassVar

from django.conf import settings
from django.db import models

from destinations.models import Attraction, Destination

# Create your models here.

class Trip(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='trips')
    name=models.CharField(max_length=150)
    start_date=models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='planning')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TripDay(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_days')
    date = models.DateField()
    day_number = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Day {self.day_number} - {self.trip.name}"


class PlannedActivity(models.Model):
    trip_day = models.ForeignKey(TripDay, on_delete=models.CASCADE, related_name='planned_activities')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='planned_activities')
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    order = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='scheduled')

    class Meta:
        ordering: ClassVar[list[str]] = ['order']

    def __str__(self):
        return f"{self.attraction.name} ({self.start_time})"

