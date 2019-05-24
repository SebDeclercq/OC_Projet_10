from django.db.utils import IntegrityError
from django.test import TestCase
from User.models import User
from Food.models import Category, Product
from Favorite.models import Favorite


class TestFavoriteModel(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            email='az@er.ty', password='azerty'
        )
        self.bad_product: Product = Product.objects.create(
            barcode='789123', name='Test product 2',
            nutrition_grade='C', url='http://example2.com',
        )
        self.good_product: Product = Product.objects.create(
            barcode='123456', name='Test product',
            nutrition_grade='A', url='http://example.com',
        )
        self.catego: Category = Category.objects.create(name='Category 1')
        self.catego.products.add(self.bad_product)
        self.catego.products.add(self.good_product)

    def test_insert_new_favorite(self) -> None:
        favorite: Favorite = Favorite.objects.create(
            substituted=self.bad_product,
            substitute=self.good_product,
            user=self.user
        )
        self.assertEqual(Favorite.objects.first(), favorite)

    def test_double_insert_rejected(self) -> None:
        with self.assertRaises(IntegrityError):
            for i in range(2):
                Favorite.objects.create(
                    substituted=self.bad_product,
                    substitute=self.good_product,
                    user=self.user
                )

    def test_multiple_users_same_favorite(self) -> None:
        Favorite.objects.create(
            substituted=self.bad_product,
            substitute=self.good_product,
            user=self.user
        )
        Favorite.objects.create(
            substituted=self.bad_product,
            substitute=self.good_product,
            user=User.objects.create(email='qw@er.ty', password='qwerty')
        )
        self.assertEqual(len(Favorite.objects.filter(user=self.user)), 1)
