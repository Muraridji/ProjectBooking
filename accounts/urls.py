from django.urls import path
from accounts import views
from config.urls import app_name

app_name = "accounts"

urlpatterns = [
    path("registrate_page/", views.register, name="register"),
    path("login_page/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]