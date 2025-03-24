from django.urls import path
from booking import views

app_name = "booking"

urlpatterns = [
    path('places/', views.PlacePageView.as_view(), name="places"),
    path('book/<int:place_id>/', views.BookPlaceView.as_view(), name="book_place"),
    path('profile/', views.UserProfileView.as_view(), name="user_profile"),
    path('api/bookings/<int:place_id>/', views.GetBookingsView.as_view(), name="get_bookings"),
    path('delete/<int:booking_id>/', views.DeleteBookingView.as_view(), name="delete_booking"),
    path('confirm/<str:token>/', views.ConfirmBookingView.as_view(), name='confirm_booking'),
]
