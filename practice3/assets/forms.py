from django import forms
from .models import Asset


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Asset
        # created_at is filled automatically, so it is not in the form.
        fields = ['asset_id','name','category','purchase_date','cost','status','location']
        widgets = {'purchase_date':forms.DateInput(attrs={'type':'date'})}
