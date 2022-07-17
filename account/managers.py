from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **extra_fields: dict):
        if not email:
            raise ValueError("The given email must be set.")

        if extra_fields.get("first_name", False):
            extra_fields["first_name"] = extra_fields["first_name"].title()

        if extra_fields.get("last_name", False):
            extra_fields["last_name"] = extra_fields["last_name"].title()

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email: str, password: str, **extra_fields: dict):
        extra_fields.setdefault("is_seller", True)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: dict):
        extra_fields.setdefault("is_seller", False)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(email, password, **extra_fields)
