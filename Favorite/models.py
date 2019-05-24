from typing import Sequence
from django.db import models
from Food.models import Product
from User.models import User
from django.utils.translation import gettext_lazy as _


class Favorite(models.Model):
    substituted: models.ForeignKey = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name=_('substituted'),
        help_text=_('Product to be substituted by')
    )
    substitute: models.ForeignKey = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name=_('substitute'),
        help_text=_('Product substituting the other')
    )
    user: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE,
        help_text=_('User which substituted a product by another')
    )

    objects: models.Manager = models.Manager()

    class Meta:
        unique_together: Sequence[Sequence[str]] = (
            ('substituted', 'substitute', 'user'),
        )
        verbose_name: str = _('favorite')
        verbose_name_plural: str = _('favorites')
