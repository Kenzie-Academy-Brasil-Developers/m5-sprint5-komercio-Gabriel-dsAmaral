from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Account


class AccountModelTest(TestCase):
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

    def test_email_unique(self):
        account = Account.objects.get(id=1)
        unique = account._meta.get_field("email").unique
        self.assertEquals(unique, True)

    def test_first_name_max_length(self):
        account = Account.objects.get(id=1)
        max_length = account._meta.get_field("first_name").max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        account = Account.objects.get(id=1)
        max_length = account._meta.get_field("last_name").max_length
        self.assertEquals(max_length, 50)

    def test_password_max_length(self):
        account = Account.objects.get(id=1)
        max_length = account._meta.get_field("password").max_length
        self.assertEquals(max_length, 128)

    def test_is_seller_default(self):
        account = Account.objects.get(id=1)
        default = account._meta.get_field("is_seller").default
        self.assertEquals(default, False)

    def test_date_joined_auto_now_add(self):
        account = Account.objects.get(id=1)
        date_joined = account._meta.get_field("date_joined").auto_now_add
        self.assertEquals(date_joined, True)


class AccountViewsTest(APITestCase):
    def test_create_account_view(self):
        response = self.client.post(
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

        self.assertEqual(response.status_code, 201)

    def test_login_view(self):

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

        response = self.client.post(
            "/api/login/",
            {
                "email": "test@mail.com",
                "password": "1234",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
