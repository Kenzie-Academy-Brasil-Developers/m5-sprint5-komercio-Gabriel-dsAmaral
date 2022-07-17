from django.urls import path
from rest_framework_simplejwt import views
from .views import (
    AccountView,
    AccountDetailView,
    AccountUpdateView,
    AccountIsActiveView,
)

urlpatterns = [
    path("accounts/", AccountView.as_view()),
    path("accounts/<int:pk>/", AccountUpdateView.as_view()),
    path("accounts/<int:pk>/management/", AccountIsActiveView.as_view()),
    path("accounts/newest/<int:num_of_accounts>/", AccountDetailView.as_view()),
    path("login/", views.TokenObtainPairView.as_view()),
    path("login/refresh/", views.TokenRefreshView.as_view()),
]
