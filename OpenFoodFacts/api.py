#!/usr/bin/env python3
'''Class interfacing the App and the OpenFoodFacts's API
@note   Copied and modified version of my OCP5 repo:
        https://github.com/SebDeclercq/OC_Projet_5/tree/master/OpenFoodFacts'''
from typing import Any, Dict, Iterator, List, Set, Union
from dataclasses import dataclass, fields
import re
import requests


@dataclass
class Product:
    '''Class representing a minimal Product from OpenFoodFacts API'''
    id: int
    name: str
    nutrition_grades: str
    url: str
    image_url: str
    image_nutrition_small_url: str

    @property
    def to_food_db(self) -> Dict[str, str]:
        return {
            'barcode': str(self.id),
            'name': self.name,
            'nutrition_grade': self.nutrition_grades.upper(),
            'url': self.url,
            'img': self._full_image_url,
            'nutrition_img': self._image_nutrition_url
        }

    @property
    def _full_image_url(self) -> str:
        return re.sub(r'\.\d+\.jpg$', '.full.jpg', self.image_url)

    @property
    def _image_nutrition_url(self) -> str:
        return re.sub(r'\.\d+\.jpg$', '.full.jpg',
                      self.image_nutrition_small_url)

class API:
    '''Class interfacing the App and the OpenFoodFacts's API
    Class attributes:
        BASE_URL:      URL to the API without parameter
        BASE_PARAMS:   Dictionary containing base parameters for the API
        USEFUL_FIELDS: Collects dynamically the Product attributes names.
                       Simplifies the collection of the wanted data only.'''
    BASE_URL: str = 'https://fr.openfoodfacts.org/cgi/search.pl'
    BASE_PARAMS: Dict[str, Union[int, str]] = {
        'action': 'process',
        'page_size': 20,
        'json': 1,
        'sort_by': 'unique_scans_n',
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
    }
    USEFUL_FIELDS: Set[str] = {
        field.name for field in fields(Product)
    }

    def _get_products(
        self, params: Dict[str, Union[int, str]]
    ) -> Iterator[Product]:
        '''Private method calling the API with the parameters provided.
        Instanciates a Product object for every products collected in
        the API response and yields them'''
        r_params: Dict[str, Union[int, str]] = self.BASE_PARAMS.copy()
        r_params.update(params)
        r_result: requests.Response = requests.get(self.BASE_URL, r_params)
        if r_result.status_code != requests.codes.ok:
            r_result.raise_for_status()
        products: List[Dict[str, Any]] = r_result.json()['products']
        for result in products:
            result['name'] = result.pop('product_name')
            if self._result_complete(result):  # If all data are available
                product: Product = Product(
                    **{k: result[k] for k in self.USEFUL_FIELDS}
                )
                yield product

    def _result_complete(self, result: Dict[str, Union[int, str]]) -> bool:
        '''Private method that checks if the collected metadata from the
        API contains every required elements (returns True/False)'''
        for field in self.USEFUL_FIELDS:
            if field not in result or not result[field]:
                return False
        return True

    def search(
        self, category: str, page: int = 1, page_size: int = 20
    ) -> Iterator[Product]:
        '''Public method to query the API based on
        a category id. Yields associated Products'''
        return self._get_products({
            'tag_0': category,
            'page': page,
            'page_size': page_size,
        })
