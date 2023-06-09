from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .models import User


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError(_("E-mail musí být vyplněný."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuživatel musí mít is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuživatel musí mít is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

    def get_user_by_uidb64(self, uidb64) -> User | None:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = self.model.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            self.model.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user
