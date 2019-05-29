#!/usr/bin/env python3
from typing import Any, List
from django.core.management.base import (BaseCommand, CommandError,
                                         CommandParser)
from django.db.utils import IntegrityError
from OpenFoodFacts.api import API
from Food.models import Category, Product


class FoodDbFeeder:
    def __init__(self, categories: List[str], nb_products: int) -> None:
        self.categories: List[str] = categories
        self.nb_products: int = nb_products
        self.api: API = API()

    def run(self) -> None:
        Category.delete_all()
        Product.delete_all()
        for category_name in self.categories:
            category: Category = Category.objects.create(name=category_name)
            self.collect_products(category)

    def collect_products(self, category: Category) -> None:
        print(f'Collecting {self.nb_products} products for "{category.name}"')
        page: int = 1
        while len(category.products.all()) < self.nb_products:
            self._collect_products(category, page)
            page += 1
        print('\n')

    def _collect_products(self, category: Category, page: int) -> None:
        for product in self.api.search(category.name, page, self.nb_products):
            if len(category.products.all()) >= self.nb_products:
                break
            try:
                category.products.add(
                    Product.objects.create(**product.to_food_db)
                )
                print('.', end='')
            except IntegrityError:
                pass


class Command(BaseCommand):
    help: str = ('Collects new data from the OpenFoodFacts API '
                 'to populate the Food DB (warning: makes clean slate)')

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--category', action='append', default=[], dest='categories',
            help='List of the expected categories in the Food DB (sep: comma)'
        )
        parser.add_argument(
            '--nb_products', '--nb_products_by_category',
            type=int, dest='nb_products', default=20,
            help='Number of the expected products by category'
        )

    def handle(self, *args: Any, **options: Any) -> None:
        if not options['categories']:
            raise CommandError('At least one --category is required')
        if not options['nb_products']:
            options['nb_products'] = 0
        food_db_feeder: FoodDbFeeder = FoodDbFeeder(
            options['categories'], options['nb_products']
        )
        food_db_feeder.run()
