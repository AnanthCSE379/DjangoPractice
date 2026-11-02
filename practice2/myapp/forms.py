from django import forms
from .models import Patient
class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ["patientid","name","admit_date","discharge_date"]
    
    
