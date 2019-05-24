import json
from typing import Any, Dict, List, Optional
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.test import Client, TestCase
from Food.models import Category, Product


class TestProductModel(TestCase):
    def setUp(self) -> None:
        self.data: Dict[str, str] = dict(
            barcode='123456', name='Test product',
            nutrition_grade='A', url='http://example.com',
            img='http://example.jpg', nutrition_img='http://example.jpg',
        )
        self.data2: Dict[str, str] = dict(
            barcode='789123', name='Test product 2',
            nutrition_grade='C', url='http://example2.com',
        )

    def test_product_insertion(self) -> None:
        product: Product = Product.objects.create(**self.data)
        self.assertEqual(Product.objects.first(), product)

    def test_product_repr(self) -> None:
        Product.objects.create(**self.data)
        product: Optional[Product] = Product.objects.first()
        if product is not None:
            self.assertEqual(
                str(product),
                f'<Product#{self.data["barcode"]} name={self.data["name"]} '
                f'nutrition_grade={self.data["nutrition_grade"]}>'
            )

    def test_substitute_manager(self) -> None:
        top_product: Product = Product.objects.create(**self.data)
        not_so_top_product: Product = Product.objects.create(**self.data2)
        self.catego: Category = Category.objects.create(name='Category 1')
        self.catego.products.add(top_product)
        self.catego.products.add(not_so_top_product)
        self.catego.save()
        substitutes: QuerySet = Product.get_substitutes_for(
            not_so_top_product
        )
        self.assertIn(top_product, substitutes)

    def test_delete_all(self) -> None:
        for data in (self.data, self.data2):
            Product.objects.create(**data)
        self.assertEqual(len(Product.objects.all()), 2)
        Product.delete_all()
        self.assertEqual(len(Product.objects.all()), 0)


class TestCategoryModel(TestCase):
    def setUp(self) -> None:
        self.product: Product = Product.objects.create(
            barcode='123456', name='Test product',
            nutrition_grade='A', url='http://example.com',
        )
        self.product2: Product = Product.objects.create(
            barcode='789123', name='Test product 2',
            nutrition_grade='C', url='http://example2.com',
        )

    def test_category_insertion(self) -> None:
        catego: Category = Category.objects.create(name='Category 1')
        self.assertEqual(Category.objects.first(), catego)

    def test_category_repr(self) -> None:
        catego: Category = Category.objects.create(name='Category 1')
        catego.products.add(self.product)
        self.assertEqual(
            str(Category.objects.first()),
            f'<Category#Category 1 products=[<Product: {self.product}>]>')

    def test_many_to_many_products(self) -> None:
        catego: Category = Category.objects.create(name='Category 1')
        catego.products.add(self.product)
        saved_catego: Optional[Category] = Category.objects.first()
        if saved_catego is not None:
            self.assertIn(self.product, saved_catego.products.all())
            self.assertIn(catego,
                          self.product.category_set.all())  # type: ignore

    def test_delete_all(self) -> None:
        for i in range(5):
            Category.objects.create(name=f'Category {i}')
        self.assertEqual(len(Category.objects.all()), 5)
        Category.delete_all()
        self.assertEqual(len(Category.objects.all()), 0)
