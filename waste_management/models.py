from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class WastePickup(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=50, default="General Waste")
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField(null=True, blank=True)
    address = models.TextField()
    assigned_picker = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    address = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.address}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="waste_profile")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
