from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import StaffLoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = StaffLoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        staff_no = form.cleaned_data["staff_no"].strip()
        password = form.cleaned_data["password"]
        user = authenticate(request, username=staff_no, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect(request.GET.get("next") or "dashboard")

        messages.error(request, "Invalid staff number or password.")

    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
