from django.db import models


class Product(models.Model):
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    account = models.ForeignKey(to="account.Account", on_delete=models.CASCADE)
