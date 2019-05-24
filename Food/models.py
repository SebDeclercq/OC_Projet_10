from __future__ import annotations
from typing import List, Sequence, Tuple
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Product(models.Model):
    NUTRITION_GRADES: Sequence[Tuple[str, str]] = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    )

    barcode: models.CharField = models.CharField(
        _('barcode'), max_length=48, blank=False, unique=True
    )
    name: models.CharField = models.CharField(
        _('product name'), max_length=500, blank=False
    )
    nutrition_grade: models.CharField = models.CharField(
        _('nutrition grade'), choices=NUTRITION_GRADES, blank=False,
        max_length=1
    )
    url: models.URLField = models.URLField(_('url'), blank=False, unique=True)
    img: models.URLField = models.URLField(_('img'), blank=True)
    nutrition_img: models.URLField = models.URLField(
        _('nutrition_img'), blank=True
    )

    objects: models.Manager = models.Manager()

    class Meta:
        ordering: Sequence[str] = ('name', 'nutrition_grade',)
        verbose_name: str = _('product')
        verbose_name_plural: str = _('products')

    def __str__(self) -> str:
        return (f'<Product#{self.barcode} name={self.name} '
                f'nutrition_grade={self.nutrition_grade}>')

    def get_substitutes_for(product: Product) -> models.query.QuerySet:
        nutrition_grades_scale: List[str] = []
        for grade, __ in Product.NUTRITION_GRADES:
            nutrition_grades_scale.append(grade)
        idx: int = nutrition_grades_scale.index(product.nutrition_grade)
        better_grades: List[str] = nutrition_grades_scale[:idx]
        return Product.objects.filter(
            nutrition_grade__in=better_grades,
            category=product.category_set.first()  # type: ignore
        ).order_by('nutrition_grade')[:6]

    def delete_all() -> None:  # type: ignore
        Product.objects.all().delete()

    @property
    def get_absolute_url(self) -> str:
        return reverse('food:product', args=[self.barcode])


class Category(models.Model):
    name: models.CharField = models.CharField(
        _('category name'), max_length=255, blank=False
    )
    products: models.ManyToManyField = models.ManyToManyField(Product)
    objects: models.Manager = models.Manager()

    class Meta:
        ordering: Sequence[str] = ('name',)
        verbose_name: str = _('category')
        verbose_name_plural: str = _('categories')

    def __str__(self) -> str:
        products: List[Product] = list(self.products.all())
        return f'<Category#{self.name} products={products}>'

    def delete_all() -> None:  # type: ignore
        Category.objects.all().delete()
