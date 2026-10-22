from django import forms
from django.utils import timezone

from accounts.models import TravelPreference

from .models import Trip


class PreferenceWizardForm(forms.ModelForm):
    class Meta:
        model = TravelPreference
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["travel_style"].choices = (
            TravelPreference.TRAVEL_STYLE_CHOICES
        )



class DestinationWizardForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = (
            "destination",
            "name",
        )


class TripDetailsWizardForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = (
            "start_date",
            "end_date",
            "budget",
            "status",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].widget = forms.DateInput(attrs={"type": "date"})
        self.fields["end_date"].widget = forms.DateInput(attrs={"type": "date"})

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        today = timezone.now().date()

        if start_date and start_date < today:
            self.add_error(
                "start_date",
                "Start date cannot be before today."
            )

        if start_date and end_date:

            if end_date < start_date:
                self.add_error(
                    "end_date",
                    "End date cannot be before the start date."
                )

            elif end_date == start_date:
                self.add_error(
                    "end_date",
                    "Trip must be at least one day long."
                )

        return cleaned_data


class ReviewForm(forms.Form):
    pass
