from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from chat.models import ChatSession
from documents.models import Document

from .forms import LoginForm, RegisterForm
from .models import User


class HomeView(TemplateView):
    template_name = "home.html"


class PricingPageView(TemplateView):
    template_name = "pricing.html"


class RegisterPageView(View):
    template_name = "accounts/register.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, self.template_name, {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            if User.objects.filter(email=email).exists():
                form.add_error("email", "This email is already registered.")
            else:
                user = User.objects.create_user(email=email, password=form.cleaned_data["password"])
                login(request, user)
                return redirect("dashboard")
        return render(request, self.template_name, {"form": form})


class LoginPageView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, self.template_name, {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect("dashboard")
            messages.error(request, "Invalid credentials.")
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class LogoutPageView(View):
    def post(self, request):
        logout(request)
        return redirect("home")


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["sessions"] = ChatSession.objects.filter(user=user).order_by("-created_at")
        context["documents"] = Document.objects.filter(user=user).order_by("-uploaded_at")
        return context
