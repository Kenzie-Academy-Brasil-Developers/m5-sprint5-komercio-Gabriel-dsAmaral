from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, authentication

from core.permissions import IsAdminOrReadOnly
from .permissions import OnlySuperUser
from .models import Account
from .serializers import AccountSerializer, AccountIsActiveSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import APIView, Request, Response, status


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetailView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        max_accounts = self.kwargs["num_of_accounts"]
        return self.queryset.order_by("-date_joined")[0:max_accounts]


class AccountUpdateView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_update(self, serializer):
        token = AccessToken(self.request.META.get("HTTP_AUTHORIZATION").split(" ")[1])
        logged = get_object_or_404(Account, pk=token["user_id"])
        passed = get_object_or_404(Account, pk=self.kwargs["pk"])
        if logged != passed:
            raise NotAuthenticated(
                detail="Logged in user different from the requested user"
            )
        return super().perform_update(serializer)


class AccountIsActiveView(APIView):
    permission_classes = [OnlySuperUser]
    authentication_classes = [authentication.TokenAuthentication]

    def patch(self, request: Request, pk: int):
        try:
            user = get_object_or_404(Account, pk=pk)
            is_active = False

            if user.is_active == False:
                is_active = True

            serialized = AccountIsActiveSerializer(
                user, {"is_active": is_active}, partial=True
            )
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response(
                {"message": "Account not found."}, status.HTTP_404_NOT_FOUND
            )
