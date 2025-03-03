from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Booking

@receiver(post_save, sender=Booking)
def send_booking_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = "Підтвердження бронювання"
        message = (
            f"Привіт, {instance.user.first_name}!\n\n"
            f"Ви успішно забронювали місце: {instance.place.title}\n"
            f"📅 Дата: {instance.start_time}\n"
            f"💰 Ціна: {instance.place.price} грн\n"
            f"📍 Локація: {instance.place}\n\n"
            f"Дякуємо за ваше бронювання!"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=False,
        )
