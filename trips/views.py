from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView

from .forms import (
    DestinationWizardForm,
    PreferenceWizardForm,
    ReviewForm,
    TripDetailsWizardForm,
)

FORMS = [
    ("preferences", PreferenceWizardForm),
    ("destination", DestinationWizardForm),
    ("details", TripDetailsWizardForm),
    ("review", ReviewForm),
]


class CreateTripView(LoginRequiredMixin, SessionWizardView):
    form_list = FORMS
    template_name = "trips/trips.html"

    def done(self, form_list, **kwargs):

        data = self.get_all_cleaned_data()

        print(data)

        return HttpResponse("Form submitted!")
