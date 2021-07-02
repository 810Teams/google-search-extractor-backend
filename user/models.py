"""
    User Application Models
    user/models.py
"""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """ User manager """
    def create_user(self, username, password=None, **kwargs):
        """ Create user """
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        """ Create superuser """
        user = self.create_user(username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User model """
    # Personal Information
    username = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)

    # User Group
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Others
    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        """ String representation """
        return self.username
