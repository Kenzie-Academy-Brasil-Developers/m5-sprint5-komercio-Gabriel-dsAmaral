from django.test import TestCase
from .models import Product
from rest_framework.test import APITestCase
from account.models import Account


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "test@mail.com"
        cls.first_name = "jonh"
        cls.last_name = "doe"
        cls.password = "1234"
        cls.is_seller = True

        cls.account = Account.objects.create(
            email=cls.email,
            first_name=cls.first_name,
            last_name=cls.last_name,
            password=cls.password,
            is_seller=cls.is_seller,
        )

        cls.description = "description"
        cls.price = 20
        cls.quantity = 1

        cls.Product = Product.objects.create(
            description=cls.description,
            price=cls.price,
            quantity=cls.quantity,
            account=cls.account,
        )

    def test_is_seller_default(self):
        product = Product.objects.get(id=1)
        default = product._meta.get_field("is_active").default
        self.assertEquals(default, True)

    def test_seller(self):
        product = Product.objects.get(id=1)
        self.assertEquals(product.account_id, 1)


class ProductViewsTest(APITestCase):
    def setUp(self):
        self.client.post(
            "/api/accounts/",
            {
                "first_name": "jonh",
                "last_name": "doe",
                "email": "test@mail.com",
                "password": "1234",
                "is_seller": True,
            },
            format="json",
        )
        token = self.client.post(
            "/api/login/",
            {
                "email": "test@mail.com",
                "password": "1234",
            },
            format="json",
        ).json()["access"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)


    def test_create_product_view(self):

        response = self.client.post(
            "/api/products/",
            {"description": "Smartband XYZ 3.0", "price": 100.99, "quantity": 15},
            format="json",
        )

        self.assertEqual(response.status_code, 201)


    def test_get_by_id_view(self):
        
        self.client.post(
            "/api/products/",
            {"description": "Smartband XYZ 3.0", "price": 100.99, "quantity": 15},
            format="json",
        )
        
        response = self.client.get(
            "/api/products/1/",
            format="json",
        )

        self.assertEqual(response.status_code, 200)