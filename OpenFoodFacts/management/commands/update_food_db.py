#!/usr/bin/env python3
from typing import Any
from django.core.management.base import BaseCommand
from OpenFoodFacts.update_db import FoodDbUpdater


class Command(BaseCommand):
    help: str = ('Collects new data from the OpenFoodFacts API '
                 'to update the Food DB records')

    def handle(self, *args: Any, **options: Any) -> None:
        print('Starting up the database update')
        food_db_updater: FoodDbUpdater = FoodDbUpdater()
        food_db_updater.run()
        print('Update complete')
