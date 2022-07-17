from django.shortcuts import get_object_or_404
from rest_framework import permissions, views
from rest_framework_simplejwt.tokens import AccessToken

from account.models import Account


class OnlySuperUser(permissions.BasePermission):
    def has_permission(self, request: views.Request, _):
        token = AccessToken(request.META.get("HTTP_AUTHORIZATION").split(" ")[1])
        account = get_object_or_404(Account, pk=token["user_id"])

        return account.is_superuser
