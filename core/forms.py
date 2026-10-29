from django import forms


class CustomSignupForm(forms.Form):
    """Collect first and last names alongside the fields managed by allauth."""
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First Name '})
    )
    last_name = forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={'placeholder': 'Last Name '})
        )

    def signup(self, request, user):
        """Copy the extra signup fields onto the newly created user account."""
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        user.save()

