#!/usr/bin/env python3
import os
from unittest import mock
from django.core.management import call_command
from django.test import TestCase
import requests
import responses
from OpenFoodFacts.update_db import FoodDbUpdater


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

    def test_init(self) -> None:
        db_updater: FoodDbUpdater = FoodDbUpdater(csv_separator=';')
        self.assertIn('openfoodfacts.org', db_updater.off_csv_url)
        self.assertEqual(';', db_updater.csv_separator)
        self.assertTrue(hasattr(db_updater, 'off_csv_file'))

    @responses.activate
    def test_get_off_csv_file(self) -> None:
        responses.add(responses.GET, self.db_updater.off_csv_url,
                      status=200, body='Hello World')
        self.db_updater.get_off_csv_file()
        self.assertTrue(os.path.isfile(self.db_updater.off_csv_file))
        self.assertGreater(os.path.getsize(self.db_updater.off_csv_file), 0)
        with open(self.db_updater.off_csv_file) as csv_fhandle:
            content: str = csv_fhandle.read()
        self.assertEqual('Hello World', content)
