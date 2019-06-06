#!/usr/bin/env python3
from dataclasses import dataclass, field, fields
from typing import Any, Dict, Iterator, Sequence
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


class DataConverter:
    @classmethod
    def csv_data_to_obj(cls, data: Dict[str, Any]) -> CsvData:
        result: Dict[str, Any] = {k: str(v) for k, v in data.items()}
        return CsvData(**result)


@dataclass
class FoodDbUpdater:
    off_csv_url: str = 'https://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv'  # noqa
    csv_separator: str = '\t'
    tmp_dir: str = tempfile.gettempdir()
    output_file: str = 'off.products.csv'
    products: Dict[str, Product] = field(default_factory=dict)

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

    def get_products_data(self) -> Iterator[CsvData]:
        self.get_products()
        with open(self.off_csv_file) as off_file:
            off_data: Any = csv.DictReader(
                off_file, delimiter=self.csv_separator
            )
            for raw_data in off_data:
                useful_data: Dict[str, Any] = self._extract_useful_data(raw_data)  # noqa
                if useful_data['code'] in self.products:
                    yield DataConverter.csv_data_to_obj(raw_data)

    def _extract_useful_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        useful_keys: Sequence[str] = (f.name for f in fields(CsvData))
        result: Dict[str, Any] = {}
        for key, val in data.items():
            if key in useful_keys:
                result[key] = val
        return result

    # def get_product_data(self, product: Product) -> CsvData:
    #     if self.full_data is None:
    #         raise ValueError('No data found')
    #     data: pd.Series = self.full_data.loc[
    #         self.full_data.code == product.barcode
    #     ]
    #     if len(data) == 1:
    #         return DataConverter.csv_data_to_obj(data)
    #     elif len(data) == 0:
    #         raise ProductNotFoundError(
    #             f'{product.name} ({product.barcode}) not found in csv file'
    #         )
    #     else:
    #         raise TooManyProducts(
    #             f'{product.name} ({product.barcode}) found '
    #             f'{len(data)} times in csv file'
    #         )


class ProductNotFoundError(Exception):
    pass


class TooManyProducts(Exception):
    pass
