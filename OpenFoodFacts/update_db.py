#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional
import os
import tempfile
from requests.models import Response
import pandas as pd
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
    def csv_data_to_obj(cls, data: pd.Series) -> CsvData:
        result: Dict[str, Any] = {}
        data.replace({pd.np.nan: None}, inplace=True)
        for param, val in data.to_dict().items():
            val = list(val.values()).pop(0)
            if isinstance(val, int):
                val = str(val)
            result[param] = val
        return CsvData(**result)


@dataclass
class FoodDbUpdater:
    off_csv_url: str = 'https://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv'  # noqa
    csv_separator: str = '\t'
    tmp_dir: str = tempfile.gettempdir()
    output_file: str = 'off.products.csv'
    full_data: Optional[pd.DataFrame] = None

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
        self.full_data: pd.DataFrame = pd.read_csv(
            self.off_csv_file, sep=self.csv_separator
        )

    @property
    def products(self) -> Iterator[Product]:
        for product in Product.objects.all():
            yield product

    def get_product_data(self, product: Product) -> CsvData:
        if self.full_data is None:
            raise ValueError('No data found')
        data: pd.Series = self.full_data.loc[
            self.full_data.code == product.barcode
        ]
        if len(data) == 1:
            return DataConverter.csv_data_to_obj(data)
