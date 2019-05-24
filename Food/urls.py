from typing import List
from django.urls import path
from django.utils.translation import gettext as _
from . import views


app_name: str = 'food'


urlpatterns: List[path] = [
    path(_('search'), views.SearchView.as_view(), name=_('search')),
    path(_('product/<int:substitute_barcode>/<int:substituted_barcode>'),
         views.ProductView.as_view(), name=_('product')),
    path(_('ajax'), views.AjaxView.as_view(), name=_('ajax')),
]
