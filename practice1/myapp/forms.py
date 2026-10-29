from django import forms
from .models import Player


class PlayerForm(forms.ModelForm):
    # Text input lets our view check the ID and show the required error page.
    id = forms.CharField(label='Player ID')
    score = forms.IntegerField(min_value=0,label='Shots stopped (Goalie) / Goals (Field Player)')

    class Meta:
        model = Player
        fields = ['id','name','player_type','count','score']
