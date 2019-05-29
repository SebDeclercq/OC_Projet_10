from typing import List, Sequence
from django.test import TestCase
from OpenFoodFacts.api import API, Product


class TestAPI(TestCase):
    def setUp(self) -> None:
        self.api: API = API()

    def test_api_get_product(self) -> None:
        allowed_grades: Sequence[str] = ('A', 'B', 'C', 'D', 'E')
        products: List[Product] = []
        for product in self.api.search('chips', 20):
            products.append(product)
            if len(products) >= 5:
                break
        for product in products:
            self.assertIn(product.nutrition_grades.upper(), allowed_grades)
            self.assertIn(product.to_food_db['nutrition_grade'],
                          allowed_grades)
