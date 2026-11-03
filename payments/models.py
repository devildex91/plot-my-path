from typing import ClassVar

from django.conf import settings
from django.db import models


class Payment(models.Model):
    """A record of a user's payment, including its Stripe transaction ID."""

    STATUS_CHOICES: ClassVar[tuple[tuple[str, str], ...]] = (
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    stripe_payment_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    
    amount = models.PositiveIntegerField()

    currency = models.CharField(
        max_length=3,
        default='gbp'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} {self.currency}"

    @property
    def amount_pounds(self):
        """Return the stored amount in pounds, assuming it is denominated in pence."""
        return self.amount / 100


class PremiumMembership(models.Model):
    """A user's premium access state and its associated payment, if available."""

    STATUS_CHOICES: ClassVar[tuple[tuple[str, str], ...]] = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('past_due', 'Past Due'),
    )

    user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='membership'
    )
    payment = models.OneToOneField(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='membership'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='inactive'
    )

    stripe_customer_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.status}"

    @property
    def is_active(self):
        """Whether the membership currently grants premium access."""
        return self.status == "active"