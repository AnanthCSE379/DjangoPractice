from django import forms
from .models import Registration


class RegistrationForm(forms.ModelForm):
    # ModelForm generates inputs and dropdowns using the model fields.
    class Meta:
        model = Registration
        fields = ['customer_name', 'mobile_number', 'email', 'apartment_name', 'flat_type']

    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number']
        # Check length and allow only the ordinary digits 0-9.
        if len(mobile) != 10 or not mobile.isdigit() or not mobile.isascii():
            raise forms.ValidationError('Enter exactly 10 numeric digits.')
        return mobile
