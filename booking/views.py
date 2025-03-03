from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.utils.dateparse import parse_date
from booking.models import Place, Booking
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def home_view(request):
    return render(request, "booking/index.html")


def get_bookings_view(request, place_id):
    bookings = Booking.objects.filter(place_id=place_id).values("start_time", "end_time")
    return JsonResponse({"bookings": list(bookings)})


from django.db.models import Q
from django.utils.dateparse import parse_date


def place_page_view(request):
    places = Place.objects.all()

    # Get filter values
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_capacity = request.GET.get('min_capacity')

    # Get date filters safely
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    start_date = parse_date(start_date_str) if start_date_str else None
    end_date = parse_date(end_date_str) if end_date_str else None

    # Apply basic filters
    if min_price:
        places = places.filter(price__gte=min_price)
    if max_price:
        places = places.filter(price__lte=max_price)
    if min_capacity:
        places = places.filter(capacity__gte=min_capacity)

    # Apply availability filter
    if start_date and end_date and start_date < end_date:
        booked_places = Booking.objects.filter(
            Q(start_time__lt=end_date, end_time__gt=start_date)
        ).values_list('place_id', flat=True)

        places = places.exclude(id__in=booked_places)

    return render(request, 'booking/place_page.html', {'places': places})


def confirm_booking(request, token):
    booking = get_object_or_404(Booking, confirmation_token=token)

    if not booking.is_confirmed:
        booking.is_confirmed = True
        booking.save()

    return HttpResponse("Ваше бронювання підтверджено!✅")


@login_required
def book_place_view(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    if not place.is_available:
        return JsonResponse({'error': 'Місце недоступне'}, status=400)

    start_date = parse_date(request.POST.get("start_date"))
    end_date = parse_date(request.POST.get("end_date"))
    username = request.POST.get("username")
    email = request.POST.get("email")

    if not start_date or not end_date or start_date >= end_date:
        return JsonResponse({'error': 'Невірні дати бронювання'}, status=400)

    if Booking.objects.filter(place=place, start_time__lt=end_date, end_time__gt=start_date).exists():
        return JsonResponse({'error': 'Дати вже зайняті'}, status=400)

    if not username or not email:
        return JsonResponse({'error': 'Ім\'я користувача та Gmail є обов\'язковими'}, status=400)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'error': 'Неправильний формат Gmail'}, status=400)

    booking = Booking.objects.create(
        user=request.user,
        place=place,
        start_time=start_date,
        end_time=end_date,
        is_confirmed=False  # Бронювання поки не підтверджене
    )

    # Формуємо URL для підтвердження бронювання
    confirmation_link = request.build_absolute_uri(
        reverse('confirm_booking', args=[booking.confirmation_token])
    )

    # Відправляємо лист
    send_mail(
        'Підтвердження бронювання',
        f'Привіт, {username}!\n\nЩоб підтвердити бронювання, перейдіть за посиланням:\n{confirmation_link}\n\nДякуємо!',
        'твій_емейл@gmail.com',
        [email],
        fail_silently=False,
    )

    return JsonResponse({'success': True, 'message': 'Перевірте пошту для підтвердження.'})

@login_required
def user_profile_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/user_profile.html', {'bookings': bookings})


@login_required
def delete_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    booking.place.is_available = True
    booking.place.save()

    booking.delete()

    return JsonResponse({"success": True})