#!/usr/bin/env python3
from typing import Any, Dict, List, Sequence, Tuple
from unittest import skip
import os
import tempfile
from django.core.management import call_command
from django.test import override_settings, TestCase
import responses  # type: ignore
from Food.models import Product
from OpenFoodFacts.update_db import CsvData, FoodDbUpdater
import Food  # noqa
import OpenFoodFacts  # noqa


class TestUpdateCommand(TestCase):
    @skip('Real life test w/ OpenFoodFacts CSV file too heavy')
    def test_update_db(self) -> None:
        try:
            call_command('update_food_db')
        except Exception as e:
            self.fail('The command "update_food_db"'
                      f' raised {e.__class__.__name__} unexpectedly')


class TestFoodDbUpdater(TestCase):
    def setUp(self) -> None:
        self.db_updater: FoodDbUpdater = FoodDbUpdater()
        self.csv_header: Sequence[str] = (
            'code', 'product_name', 'nutrition_grade_fr', 'url', 'image_url'
        )
        self.csv_data: Sequence[Sequence[str]] = (
            ('123', 'Product 1', 'B', 'www.url1.org', 'www.img1.com'),
            ('456', 'Product 2', 'A', 'www.url2.org', 'www.img2.com'),
            ('789', 'Product 3', 'C', 'www.url3.org', 'www.img3.com'),
        )
        for (barcode, name, grade, url, _) in self.csv_data[:3]:
            Product.objects.create(barcode=barcode, name=name,
                                   nutrition_grade=grade, url=url)
        self.csv_content: str = '\n'.join((
            self.db_updater.csv_separator.join(self.csv_header),
            *[self.db_updater.csv_separator.join(row)
                for row in self.csv_data]
        ))

    def test_init(self) -> None:
        db_updater: FoodDbUpdater = FoodDbUpdater(csv_separator=';')
        self.assertIn('openfoodfacts.org', db_updater.off_csv_url)
        self.assertEqual(';', db_updater.csv_separator)
        self.assertTrue(hasattr(db_updater, 'off_csv_file'))

    @responses.activate
    def test_get_off_csv_file(self) -> None:
        responses.add(responses.GET, self.db_updater.off_csv_url,
                      status=200, body=self.csv_content)
        self.db_updater.get_off_csv_file()
        self.assertTrue(os.path.isfile(self.db_updater.off_csv_file))
        self.assertGreater(os.path.getsize(self.db_updater.off_csv_file), 0)
        with open(self.db_updater.off_csv_file) as csv_fhandle:
            content: str = csv_fhandle.read()
        self.assertEqual(self.csv_content, content)

    @responses.activate
    def test_get_off_csv_file_error_404(self) -> None:
        responses.add(responses.GET, self.db_updater.off_csv_url, status=404)
        with self.assertRaises(FileNotFoundError):
            self.db_updater.get_off_csv_file()

    def test_get_product_ids_in_db(self) -> None:
        self.db_updater.get_products()
        for product in Product.objects.all():
            self.assertIn(product.barcode, self.db_updater.products.keys())
            self.assertIn(product, self.db_updater.products.values())

    def _test_extract_useful_data(self) -> None:
        data: Dict[str, str] = {'code': 'azer', 'fake': 'ty'}
        self.assertEqual(1, len(self.db_updater._extract_useful_data(data)))

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_get_products_data_in_csv(self) -> None:
        temp_filename: str = os.path.join(
            tempfile.gettempdir(), self.db_updater.off_csv_file
        )
        with open(temp_filename, 'w') as temp_file:
            temp_file.write(self.csv_content)
        self.db_updater.products = {
            p.barcode: p for p in Product.objects.all()[:2]
        }
        full_data: List[Tuple[Product, CsvData]] = list(
            self.db_updater.get_products_data()
        )
        products: Sequence[Product] = tuple(p for (p, _) in full_data)
        csv_data: Sequence[CsvData] = tuple(c for (_, c) in full_data)
        for data in self.csv_data[:2]:
            dict_data: Dict[str, Any] = dict(zip(
                self.csv_header, data
            ))
            self.assertIn(CsvData(**dict_data), csv_data)
        for product in Product.objects.all()[:2]:
            self.assertIn(product, products)

    def test_update_product(self) -> None:
        product: Product = Product.objects.filter(barcode='123')[0]
        old_url: str = product.url
        old_img: str = product.img
        data: CsvData = CsvData(
            '123', 'Product 1', 'A', 'www.new_url1.org', 'www.new_img1.com'
        )
        self.db_updater.update_product(product, data)
        updated_product: Product = Product.objects.filter(barcode='123')[0]
        self.assertNotEqual(old_url, updated_product.url)
        self.assertNotEqual(old_img, updated_product.url)
        self.assertEqual(data.url, updated_product.url)
        self.assertEqual(data.image_url, updated_product.img)
