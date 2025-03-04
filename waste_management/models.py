from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class WastePickup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=50, default="General Waste")  # Add a default value
    pickup_date = models.DateField()
    pickup_time = models.TimeField(default="00:00:00")  # Ensure default time is set
    address = models.TextField()
    status = models.CharField(max_length=20, default="Pending")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.address}"
