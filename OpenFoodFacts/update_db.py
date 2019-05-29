#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Iterator
import os
import tempfile
from requests.models import Response
import requests
from Food.models import Product


@dataclass
class FoodDbUpdater:
    off_csv_url: str = 'https://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv'  # noqa
    csv_separator: str = '\t'
    tmp_dir: str = tempfile.gettempdir()
    output_file: str = 'off.products.csv'

    @property
    def off_csv_file(self) -> str:
        return os.path.join(self.tmp_dir, self.output_file)

    def run(self) -> None:
        ...

    def get_off_csv_file(self) -> None:
        resp: Response = requests.get(self.off_csv_url)
        if resp.status_code == 200:
            with open(self.off_csv_file, 'w') as csv_fhandle:
                csv_fhandle.write(resp.text)
        else:
            raise FileNotFoundError(f'{self.off_csv_url} is unavailable')

    @property
    def products(self) -> Iterator[Product]:
        for product in Product.objects.all():
            yield product
