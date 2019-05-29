#!/usr/bin/env python3
from typing import Any, Dict, Sequence
from unittest import mock
import os
import tempfile
import types
from django.core.management import call_command
from django.test import override_settings, TestCase
import pandas as pd
import responses
from Food.models import Product
from OpenFoodFacts.update_db import (CsvData, FoodDbUpdater,
                                     ProductNotFoundError, TooManyProducts)
import Food  # noqa


class TestUpdateCommand(TestCase):
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
            'code', 'product_name', 'nutrition_grade', 'url', 'image_url'
        )
        self.csv_data: Sequence[Sequence[str]] = (
            ('123', 'Product 1', 'B', 'www.url1.org', 'www.img1.com'),
            ('346', 'Product 2', 'A', 'www.url2.org', ''),
        )
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
        for i in range(3):
            Product.objects.create(barcode=i, name=f'Product {i}',
                                   nutrition_grade='A', url=f'www.url{i}.org')
        self.assertIsInstance(self.db_updater.products, types.GeneratorType)
        self.assertIsInstance(next(self.db_updater.products), Product)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_get_product_data_in_csv(self) -> None:
        temp_filename: str = os.path.join(
            tempfile.gettempdir(), self.db_updater.off_csv_file
        )
        with open(temp_filename, 'w') as temp_file:
            temp_file.write(self.csv_content)
        product_2: Product = Product(
            barcode=346, name='Product 2', nutrition_grade='B',
            url='www.old_url.com'
        )
        self.db_updater.full_data = pd.read_csv(
            temp_filename, sep=self.db_updater.csv_separator
        )
        dict_data: Dict[str, Any] = dict(zip(
            self.csv_header, self.csv_data[1]
        ))
        for key, val in dict_data.items():
            if not val:
                dict_data[key] = None
        self.assertEqual(CsvData(**dict_data),
                         self.db_updater.get_product_data(product_2))

    def test_no_data_at_all(self) -> None:
        with self.assertRaises(ValueError):
            self.db_updater.get_product_data(Product())

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_no_product_data_in_csv(self) -> None:
        temp_filename: str = os.path.join(
            tempfile.gettempdir(), self.db_updater.off_csv_file
        )
        with open(temp_filename, 'w') as temp_file:
            temp_file.write(self.csv_content)
        self.db_updater.full_data = pd.read_csv(
            temp_filename, sep=self.db_updater.csv_separator
        )
        unknown_product: Product = Product(barcode='not_found')
        with self.assertRaises(ProductNotFoundError):
            self.db_updater.get_product_data(unknown_product)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_too_many_products_data_in_csv(self) -> None:
        temp_filename: str = os.path.join(
            tempfile.gettempdir(), self.db_updater.off_csv_file
        )
        with open(temp_filename, 'w') as temp_file:
            temp_file.write(self.csv_content + '\n')
            temp_file.write(self.csv_content)
        self.db_updater.full_data = pd.read_csv(
            temp_filename, sep=self.db_updater.csv_separator
        )
        product: Product = Product(barcode='346')
        with self.assertRaises(TooManyProducts):
            self.db_updater.get_product_data(product)
