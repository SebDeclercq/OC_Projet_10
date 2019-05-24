from typing import Optional
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from Favorite.models import Favorite
from Food.models import Product
from User.models import User


class SaveView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user  # type: ignore
        if user.is_authenticated:
            substituted: Optional[Product] = Product.objects.filter(
                barcode=request.POST.get('substituted')
            ).first()
            substitute: Optional[Product] = Product.objects.filter(
                barcode=request.POST.get('substitute')
            ).first()
            Favorite.objects.create(
                user=user,
                substituted=substituted,
                substitute=substitute
            )
            return JsonResponse({
                'status': 'success',
                'substitute': model_to_dict(substitute),  # type: ignore
                'substituted': model_to_dict(substituted)  # type: ignore
            })
        return JsonResponse({'status': 'error'})


class DeleteView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user  # type: ignore
        if user.is_authenticated:
            favorite: QuerySet = Favorite.objects.filter(
                    user=user,
                    substituted__barcode=request.POST.get('substituted'),
                    substitute__barcode=request.POST.get('substitute'),
            )
            favorite.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})


class FavoriteListView(View):
    favorites_list_template: str = 'Favorite/list.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user  # type: ignore
        favorites: QuerySet = Favorite.objects.filter(
            user=user
        ).all()
        return render(request, self.favorites_list_template, {
            'favorites': favorites
        })
