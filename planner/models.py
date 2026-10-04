
from django.conf import settings
from django.db import models

from destinations.models import Attraction
from trips.models import Trip


class Recommendation(models.Model):
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='recommendations')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='recommendations')
    
    
    score = models.DecimalField(max_digits=5, decimal_places=2)
    reason = models.TextField(max_length=200)
    
   
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        ordering = ('-score',)

    def __str__(self):
        return f"Rec for {self.user.username}: {self.attraction.name} (Score: {self.score})"
