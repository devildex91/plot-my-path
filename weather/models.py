from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from destinations.models import Destination


class WeatherSnapshot(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='weather_snapshots')
    

    month = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Month number from 1 (January) to 12 (December)"
    )
    
  
    avg_temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="Average temp for this month")
    avg_feels_like = models.DecimalField(max_digits=5, decimal_places=2)
    typical_condition = models.CharField(max_length=100, help_text="e.g., Sunny, Rainy, Snow")
    avg_humidity = models.IntegerField() 
    avg_wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    avg_uv_index = models.DecimalField(max_digits=4, decimal_places=1)
    
    retrieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        unique_together = ('destination', 'month')
        ordering = ('month',)

    def __str__(self):
        return f"{self.destination.name} - Month {self.month} ({self.avg_temperature}°C)"
