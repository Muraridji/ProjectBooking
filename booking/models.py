from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE
from django import forms


User = get_user_model()


class Location(models.Model):
    pass


class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, related_name="bookings", on_delete=CASCADE)

    def __str__(self):
        return f"Booking made by {self.user}"

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"


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