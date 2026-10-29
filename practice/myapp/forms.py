from django import forms
from .models import StaffPersonal
import re

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = StaffPersonal
        fields = ['staffid','name','age','mobile','mail','dept']
    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile']

        if (len(mobile) != 10 or not mobile.isdigit()):
            raise forms.ValidationError("Phone number is invalid")
        return mobile
    def clean_mail(self):
        mail = self.cleaned_data['mail']

        if (not re.match(r'[0-9a-zA-Z]+@[a-z]+.[a-z]+',mail)):
            forms.ValidationError("Invalid email")
        return mail
            
        
