from django import forms
from yatra.models import Destination

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'img1', 'img2', 'city']
