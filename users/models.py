from django.contrib.auth import password_validation
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser):
    user_name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    email = models.EmailField(
        max_length=200,
        unique=True,
        validators=[validate_email],
        verbose_name="Эл. почта",
    )
    password = models.CharField(_("password"), max_length=128)
    is_verify = models.BooleanField(default=False, null=True)
    otp_expiration = models.DateTimeField(
        null=True, blank=True, verbose_name="Срок кода"
    )
    otp = models.PositiveIntegerField(null=True)

    objects = BaseUserManager()

    class Meta:
        verbose_name = "Мои пользователи"
        verbose_name_plural = "Пользователи"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def __str__(self):
        return f"{self.user_name} {self.email}"
