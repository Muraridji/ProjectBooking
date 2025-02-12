from django.shortcuts import render
from booking.models import Place, Booking

# Create your views here.
def home_view(request):
    return render(request, "booking/index.html")

def place_page_view(request):
    places = Place.objects.all()
    return render(request, 'booking/place_page.html', {'places': places})