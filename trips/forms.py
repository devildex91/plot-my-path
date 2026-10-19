from django import forms

from accounts.models import TravelPreference

from .models import Trip


class PreferenceWizardForm(forms.ModelForm):
    class Meta:
        model = TravelPreference

        exclude = ("user",)


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

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date cannot be before the start date.")

        return cleaned_data


class ReviewForm(forms.Form):
    pass
