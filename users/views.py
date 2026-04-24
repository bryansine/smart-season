from .models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import UserRegisterForm, UserLoginForm
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class CoordinatorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_coordinator or self.request.user.is_superuser)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "Access denied. Coordinator privileges required.")
            return redirect('home')
        return super().handle_no_permission()

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully. Please log in to access the monitoring system.")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = "users/login.html"

    def get_success_url(self):
 
        return reverse_lazy("home")

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "users/profile.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)