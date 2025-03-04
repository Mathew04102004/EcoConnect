from django import forms
from .models import WastePickup

class WastePickupForm(forms.ModelForm):
    class Meta:
        model = WastePickup
        fields = ['address', 'scheduled_date', 'waste_type']
