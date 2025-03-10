from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE
from django import forms
import uuid
from django.contrib.auth.models import User


User = get_user_model()


class Location(models.Model):
    pass

class Place(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    price = models.IntegerField()
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Place {self.title}"

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"

class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, related_name="bookings", on_delete=CASCADE)
    place = models.ForeignKey(Place, related_name="bookings", on_delete=CASCADE)
    is_confirmed = models.BooleanField(default=False)
    confirmation_token = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return f"Booking by {self.user.username} at {self.place.title} from {self.start_time} to {self.end_time}"

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
