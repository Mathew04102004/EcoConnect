from django.db import models
from django.contrib.auth.models import User

class WastePickup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Check if this exists
    address = models.TextField()
    pickup_date = models.DateField()  # Check if this is named 'date' in your code
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Completed", "Completed")])

    def __str__(self):
        return f"{self.user.username} - {self.pickup_date}"
