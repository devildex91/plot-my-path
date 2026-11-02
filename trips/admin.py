from django.contrib import admin

from .models import PlannedActivity, Trip, TripDay

# Register your models here.

admin.site.register(Trip)

admin.site.register(TripDay)

admin.site.register(PlannedActivity)
