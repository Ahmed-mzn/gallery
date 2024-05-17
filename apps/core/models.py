from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email should be provided"))

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    PLAN_ACTIVE = 'active'
    PLAN_CANCELLED = 'cancelled'

    CHOICES_PLAN_STATUS = (
        (PLAN_ACTIVE, 'Active'),
        (PLAN_CANCELLED, 'Cancelled')
    )

    email = models.EmailField(max_length=85, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    plan = models.ForeignKey(Plan, related_name='plan_users', on_delete=models.SET_NULL, null=True, blank=True)
    plan_status = models.CharField(max_length=20, choices=CHOICES_PLAN_STATUS, default=PLAN_ACTIVE)
    plan_end_date = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"<User {self.email} />"


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, related_name='roles', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name='role_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} | {self.role}"
