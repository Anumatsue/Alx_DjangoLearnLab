
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegistrationForm, UserUpdateForm, ProfileForm

class BlogLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True  # already logged in? send them away

class BlogLogoutView(LogoutView):
    next_page = reverse_lazy("login")

def register(request):
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account was created.")
            return redirect("profile")
    else:
        form = RegistrationForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
    return render(request, "blog/profile.html", {"u_form": u_form, "p_form": p_form})

