from django import forms
from django.contrib.auth.models import User
from EcoConnect.models import WastePickup  # Use the correct app name


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

class WastePickupForm(forms.ModelForm):
    class Meta:
        model = WastePickup
        fields = ["address", "pickup_date"]
