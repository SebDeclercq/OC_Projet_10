from typing import List
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.utils.translation import gettext as _
from . import views


app_name: str = 'favorite'


urlpatterns: List[path] = [
    path(_('save'), views.SaveView.as_view(), name=_('save')),
    path(_('delete'), views.DeleteView.as_view(), name=_('delete')),
    path(_('list'), login_required(views.FavoriteListView.as_view()),
         name=_('list')),
]
