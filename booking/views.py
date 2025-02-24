from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.utils.dateparse import parse_date
from booking.models import Place, Booking


def home_view(request):
    return render(request, "booking/index.html")

def get_bookings_view(request, place_id):
    bookings = Booking.objects.filter(place_id=place_id).values("start_time", "end_time")
    return JsonResponse({"bookings": list(bookings)})

def place_page_view(request):
    places = Place.objects.filter(is_available=True)
    capacity = request.GET.get('capacity')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if capacity:
        places = places.filter(capacity__gte=int(capacity))
    if min_price:
        places = places.filter(price__gte=int(min_price))
    if max_price:
        places = places.filter(price__lte=int(max_price))

    return render(request, 'booking/place_page.html', {'places': places})

@login_required
def book_place_view(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    if not place.is_available:
        return JsonResponse({'error': 'Місце недоступне'}, status=400)

    start_date = parse_date(request.POST.get("start_date"))
    end_date = parse_date(request.POST.get("end_date"))

    if not start_date or not end_date or start_date >= end_date:
        return JsonResponse({'error': 'Невірні дати бронювання'}, status=400)

    if Booking.objects.filter(place=place, start_time__lt=end_date, end_time__gt=start_date).exists():
        return JsonResponse({'error': 'Дати вже зайняті'}, status=400)

    Booking.objects.create(user=request.user, place=place, start_time=start_date, end_time=end_date)

    return JsonResponse({'success': True})


@login_required
def user_profile_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/user_profile.html', {'bookings': bookings})