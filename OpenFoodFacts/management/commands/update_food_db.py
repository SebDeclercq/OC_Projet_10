#!/usr/bin/env python3
from datetime import datetime
from typing import Any
import os
from django.core.management.base import BaseCommand
from OpenFoodFacts.update_db import FoodDbUpdater


class Command(BaseCommand):
    help: str = ('Collects new data from the OpenFoodFacts API '
                 'to update the Food DB records')

    def handle(self, *args: Any, **options: Any) -> None:
        '''Main method of custom command'''
        self._display_info(datetime.now(), action='start')
        food_db_updater: FoodDbUpdater = FoodDbUpdater()
        food_db_updater.run()
        self._display_info(datetime.now(), action='end')

    def _display_info(self, time: datetime, action: str) -> None:
        '''Display info on screen and in logfile'''
        self._create_log_dir()
        msg: str = f'{action.upper():5}: {self._fmt_time(time)}'
        print(msg)
        with open(os.path.join('log', 'history.log'), 'a') as log:
            log.write(f'{msg}\n')

    def _create_log_dir(self) -> None:
        '''Create log directory if not exists'''
        if not os.path.isdir('log'):
            os.mkdir('log')

    def _fmt_time(self, time: datetime) -> str:
        '''Format a datetime object in string'''
        return time.strftime('%Y-%m-%d %H:%M:%S')
