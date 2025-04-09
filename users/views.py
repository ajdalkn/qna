from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import RegisterForm


class LoginView(AuthLoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        # Must logout any active logged in sessions in the browser before
        # logging in again.
        if request.user and request.user.is_authenticated:
            logout(request)
        return super().get(request, *args, **kwargs)


class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('login')


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        # Auto-login after registration
        login(self.request, user)
        return super().form_valid(form)
