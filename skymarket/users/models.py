from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from users.managers import UserManager


class UserRoles(models.TextChoices):
    ADMIN = ("admin", "администратор")
    USER = ("user", "пользователь")


class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "role"]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=100, db_index=True, unique=True)
    role = models.CharField(max_length=25, choices=UserRoles.choices, default=UserRoles.USER)
    image = models.ImageField(upload_to="users_img/", null=True, blank=True)
    is_active = models.BooleanField(default=False)

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
