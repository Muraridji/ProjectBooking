from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, TemplateView
from booking.models import Place, Booking
from .forms import PlaceFilterForm, BookingForm


class HomeView(TemplateView):
    template_name = "booking/index.html"

class GetBookingsView(View):
    def get(self, request, place_id):
        bookings = Booking.objects.filter(place_id=place_id).values("start_time", "end_time")
        return JsonResponse({"bookings": list(bookings)})


class PlacePageView(ListView):
    model = Place
    template_name = "booking/place_page.html"
    context_object_name = "places"
    ordering = ['-price']

    def get_queryset(self):

        filter_form = PlaceFilterForm(self.request.GET)
        queryset = Place.objects.filter(is_available=True)

        if filter_form.is_valid():
            price = filter_form.cleaned_data.get('price')
            capacity = filter_form.cleaned_data.get('capacity')
            start_time = filter_form.cleaned_data.get('start_time')
            end_time = filter_form.cleaned_data.get('end_time')


            if price:
                queryset = queryset.filter(price__lte=price)
            if capacity:
                queryset = queryset.filter(capacity__gte=capacity)

            if start_time and end_time and start_time < end_time:
                booked_places = Booking.objects.filter(
                    Q(start_time__lt=end_time, end_time__gt=start_time)
                ).values_list('place_id', flat=True)

                queryset = queryset.exclude(id__in=booked_places)

        self.filter_form = filter_form
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        initial_data = {}
        if user.is_authenticated:
            initial_data['username'] = user.username
            initial_data['email'] = user.email

        context["filter_form"] = self.filter_form
        context["booking_form"] = BookingForm(initial=initial_data)
        return context





class ConfirmBookingView(View):
    def get(self, request, token):
        booking = get_object_or_404(Booking, confirmation_token=token)
        if not booking.is_confirmed:
            booking.is_confirmed = True
            booking.save()
        return HttpResponse("Ваше бронювання підтверджено!✅")


@method_decorator(login_required, name='dispatch')
class BookPlaceView(View):
    def post(self, request, place_id):
        place = get_object_or_404(Place, id=place_id)
        if not place.is_available:
            return JsonResponse({'error': 'Місце недоступне', 'message': 'Це місце наразі не доступне для бронювання.'}, status=400)
        
        form = BookingForm(request.POST)
        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            if start_time >= end_time:
                return JsonResponse({'error': 'Невірні дати бронювання', 'message': 'Дата початку не може бути пізніше за дату закінчення.'}, status=400)
            
            if Booking.objects.filter(place=place, start_time__lt=end_time, end_time__gt=start_time).exists():
                return JsonResponse({'error': 'Дати вже зайняті', 'message': 'Ці дати вже заброньовані.'}, status=400)
            
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'error': 'Неправильний формат Gmail', 'message': 'Ваш email має неправильний формат.'}, status=400)
            
            booking = Booking.objects.create(
                user=request.user,
                place=place,
                start_time=start_time,
                end_time=end_time,
                is_confirmed=False
            )
            
            confirmation_link = request.build_absolute_uri(reverse('confirm_booking', args=[booking.confirmation_token]))
            send_mail(
                'Підтвердження бронювання',
                f'Привіт, {username}!\n\nЩоб підтвердити бронювання, перейдіть за посиланням:\n{confirmation_link}\n\nДякуємо!',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({'success': True, 'message': 'Перевірте пошту для підтвердження.'})
        
        return JsonResponse({'error': 'Невірні дані форми', 'message': 'Форма має помилки.', 'details': form.errors}, status=400)




@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    template_name = 'booking/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookings'] = Booking.objects.filter(user=self.request.user, is_confirmed=True)
        return context


@method_decorator(login_required, name='dispatch')
class DeleteBookingView(View):
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.delete()
        return JsonResponse({"success": True})
