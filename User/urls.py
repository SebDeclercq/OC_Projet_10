from typing import List
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.utils.translation import gettext as _
from . import views


app_name: str = 'user'


urlpatterns: List[path] = [
    path(_('login'), views.LoginView.as_view(), name=_('login')),
    path(_('logout'),
         login_required(views.LogoutView.as_view()),
         name=_('logout')),
    path(_('signup'), views.SignUpView.as_view(), name=_('signup')),
    path(_('account'),
         login_required(views.AccountView.as_view()),
         name=_('account')),
]
