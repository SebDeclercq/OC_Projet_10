from typing import List
from django.urls import path
from django.utils.translation import gettext as _
from . import views


app_name: str = 'app'


urlpatterns: List[path] = [
    path(_(''), views.IndexView.as_view(), name=_('index')),
    path(_('legal'), views.LegalNoticeView.as_view(), name=_('legal_notice')),
]
