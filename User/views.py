from typing import Any, Optional, Type
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView, View
from .forms import SignUpForm
from .models import User


class LoginView(TemplateView):
    template_name: str = 'login.html'

    def post(
            self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        email: Optional[str] = request.POST.get('email')
        password: Optional[str] = request.POST.get('password')
        user: Optional[User] = authenticate(  # type: ignore
            username=email, password=password
        )
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, {'wrong_credentials': True})


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect('/')


class SignUpView(CreateView):
    model: Type[User] = User
    template_name: str = 'signup.html'
    form_class: Type[SignUpForm] = SignUpForm
    success_url: str = '/'

    def form_valid(self, form: SignUpForm) -> HttpResponse:
        valid = super(SignUpView, self).form_valid(form)
        user: Optional[User] = authenticate(  # type: ignore
            firstname=form.cleaned_data.get('firstname'),
            username=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password1')
        )
        if user is not None and user.is_active:
            login(self.request, user)
        return valid


class AccountView(View):
    template_name: str = 'account.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)
