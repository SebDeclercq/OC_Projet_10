#!/usr/bin/env python3
from django.core.management import call_command
from django.test import TestCase


class TestUpdateCommand(TestCase):
    def test_update_db(self) -> None:
        try:
            call_command('update_food_db')
        except Exception as e:
            self.fail('The command "update_food_db"'
                      f' raised {e.__class__.__name__} unexpectedly')
