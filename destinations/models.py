from django.conf import settings
from django.db import models

# Create your models here.

#custom manager to fix foreign key error when loading initial data into database
class CountryManager(models.Manager):
    def get_by_natural_key(self,name):
        return self.get(name=name)


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, help_text="ISO country code")
    continent = models.CharField(max_length=50)
# tells django to use manager for natural keys lookup
    objects = CountryManager()
 # lets django know what the natural key is
    def natural_key(self):
        return(self.name,)

    def __str__(self):
        return self.name

class DestinationManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Destination(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='destinations')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    average_cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    objects = DestinationManager()
    # allows me to treate images like a database field when calling without storing image in db
    @property
    def get_image_url(self):
        cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'dxhclnrp')
        return f"https://res.cloudinary.com/{cloud_name}/image/upload/v1/{self.slug}"
    
    def natural_key(self):
        return (self.slug,)
     
    def __str__(self):
        return self.name


class Attraction(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    category = models.CharField(max_length = 50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    average_visit_minutes = models.IntegerField()
    entry_cost = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    opening_time = models.TimeField(auto_now=False, auto_now_add=False)
    closing_time = models.TimeField(auto_now=False, auto_now_add=False)

    class Meta:
        unique_together = ('destination', 'slug')

    @property
    def get_image_url(self):
        # Safely fetches just the text name from your settings configuration
        cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'dxhclnrp')
        # TARGETS THE 'attractions' FOLDER:
        return f"https://res.cloudinary.com{cloud_name}/image/upload/v1/{self.slug}"
    
    def __str__(self):
        return self.name





