from django.db import models
from django.contrib.auth.models import User

class WastePickup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Check if this exists
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField()
    pickup_date = models.DateField()  
    pickup_time = models.TimeField(null=True, blank=True)
    waste_type = models.CharField(max_length=50)
    assigned_picker = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Completed", "Completed")])

    def __str__(self):
        return f"{self.user.username} - {self.pickup_date}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username