from django.shortcuts import get_object_or_404
from rest_framework import permissions, views
from rest_framework_simplejwt.tokens import AccessToken

from account.models import Account


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: views.Request, _):
        if request.method in permissions.SAFE_METHODS:
            return True

        token = AccessToken(request.META.get("HTTP_AUTHORIZATION").split(" ")[1])
        account = get_object_or_404(Account, pk=token["user_id"])

        if account.is_seller or request.user.is_superuser == True:
            return True
        else:
            return False
