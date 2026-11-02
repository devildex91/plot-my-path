from django.contrib import admin

from .models import Payment, PremiumMembership

admin.site.register(Payment)
admin.site.register(PremiumMembership)
