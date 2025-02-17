from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from booking.models import Place, Booking


# Create your views here.
def home_view(request):
    return render(request, "booking/index.html")

def place_page_view(request):
    places = Place.objects.filter(is_available=True)
    return render(request, 'booking/place_page.html', {'places': places})

@login_required
def book_place_view(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    if not place.is_available:
        return JsonResponse({'error': 'Place is not available'}, status=400)

    # Create a new booking
    booking = Booking.objects.create(
        user=request.user,
        place=place,
        start_time=now(),
        end_time=now() + timedelta(days=1)  # Example: booking duration of 1 day
    )
    
    # Mark the place as unavailable
    place.is_available = False
    place.save()

    return JsonResponse({'success': True})


@login_required
def user_profile_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/user_profile.html', {'bookings': bookings})