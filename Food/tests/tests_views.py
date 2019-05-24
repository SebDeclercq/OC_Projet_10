import json
from typing import Any, Dict, List, Optional
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase
from Food.models import Category, Product


class TestSearchView(TestCase):
    URL: str = '/food/search'

    def setUp(self) -> None:
        self.client: Client = Client()
        self.bad_product: Product = Product.objects.create(
            barcode='789123', name='Bad Product',
            nutrition_grade='C', url='http://example2.com',
        )
        self.good_product: Product = Product.objects.create(
            barcode='123456', name='Good Product',
            nutrition_grade='A', url='http://example.com',
        )
        self.catego: Category = Category.objects.create(name='Category 1')
        self.catego.products.add(self.bad_product)
        self.catego.products.add(self.good_product)

    def test_post_data_for_search(self) -> None:
        response: HttpResponse = self.client.post(self.URL, {
            'food_search': 'Bad Product'
        })
        self.assertTemplateUsed(response, 'Food/products.html')

    def test_product_urls(self) -> None:
        response: HttpResponse = self.client.post(self.URL, {
            'food_search': 'Bad Product'
        })
        self.assertContains(response, self.good_product.name)


class TestProductView(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()
        self.good_product: Product = Product.objects.create(
            barcode='123456', name='Good Product',
            nutrition_grade='A', url='http://example.com',
        )
        self.bad_product: Product = Product.objects.create(
            barcode='789123', name='Bad Product',
            nutrition_grade='C', url='http://example2.com',
        )

    def test_product_detail(self) -> None:
        response: HttpResponse = self.client.get(
            '/food/product/'
            f'{self.good_product.barcode}/{self.bad_product.barcode}'
        )
        self.assertTemplateUsed(response, 'Food/details.html')
