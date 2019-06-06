#!/usr/bin/env python3
from dataclasses import dataclass, field, fields
from typing import Any, Dict, Iterator, Set, Tuple
import csv
import os
import tempfile
from requests.models import Response
import requests
from Food.models import Product


@dataclass
class CsvData:
    code: str
    product_name: str
    nutrition_grade: str
    url: str
    image_url: str


@dataclass
class FoodDbUpdater:
    off_csv_url: str = 'https://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv'  # noqa
    csv_separator: str = '\t'
    tmp_dir: str = tempfile.gettempdir()
    output_file: str = 'off.products.csv'
    products: Dict[str, Product] = field(default_factory=dict)
    matching_csv_db: Dict[str, str] = field(default_factory=lambda: {
        'code': 'barcode', 'product_name': 'name',
        'nutrition_grade': 'nutrition_grade', 'url': 'url', 'image_url': 'img'
    })

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

    def get_products(self) -> Dict[str, Product]:
        for product in Product.objects.all():
            self.products[product.barcode] = product
        return self.products

    def get_products_data(self) -> Iterator[Tuple[Product, CsvData]]:
        self.get_products()
        with open(self.off_csv_file) as off_file:
            off_data: Any = csv.DictReader(
                off_file, delimiter=self.csv_separator
            )
            for raw_data in off_data:
                barcode: str = raw_data['code']
                if barcode in self.products:
                    yield (self.products[barcode], CsvData(**raw_data))

    def _extract_useful_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        useful_keys: Set[str] = {f.name for f in fields(CsvData)}
        result: Dict[str, Any] = {}
        for key, val in data.items():
            if key in useful_keys:
                result[key] = val
        return result

    def update_product(self, product: Product, data: CsvData) -> None:
        for csv_attr, db_attr in self.matching_csv_db.items():
            setattr(product, db_attr, getattr(data, csv_attr))
