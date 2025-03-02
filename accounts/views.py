from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.conf import settings
from accounts.forms import RegisterForm, LoginForm
from booking.models import Place, Booking

def register(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'accounts/registrate_page.html', {'form':form})

    elif request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()
    return render(request, "accounts/registrate_page.html", {"form":form})


from django.contrib import messages


def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'accounts/login_page.html', {'form': form})

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Неправильное имя пользователя или пароль.")

        return render(request, "accounts/login_page.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")