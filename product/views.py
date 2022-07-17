from django.http import Http404
from django.shortcuts import get_object_or_404
from account.models import Account
from core.permissions import IsAdminOrReadOnly
from rest_framework.views import Response, status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import generics, authentication
from rest_framework.exceptions import NotAuthenticated
from .models import Product
from .serializers import ProductSerializer


class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer: ProductSerializer):
        token = AccessToken(self.request.META.get("HTTP_AUTHORIZATION").split(" ")[1])
        account = get_object_or_404(Account, pk=token["user_id"])
        if account.is_seller == False:
            raise NotAuthenticated(detail="You are not a Salesman")
        serializer.save(account=account)


class ProductDetailView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_update(self, serializer):
        token = AccessToken(self.request.META.get("HTTP_AUTHORIZATION").split(" ")[1])
        account = get_object_or_404(Account, pk=token["user_id"])
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        if product.account != account:
            raise NotAuthenticated(detail="You do not own this product")
        return super().perform_update(serializer)
