"""
Account models module.
"""
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """
    Manages type of created user.
    ...
    Methods:
        create_user(email, name, terms_conditions, password=None, password2=None):
            POST method for user registration.
    """

    def create_user(self, email, name, terms_conditions,
                    is_admin=False, password=None, password2=None):
        """
        Creates and saves a User with the given data.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            terms_conditions=terms_conditions,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, terms_conditions,
                         is_admin=True, password=None, password2=None):
        """
        Creates and saves a superuser with the given data.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.create_user(
            email,
            password=password,
            name=name,
            terms_conditions=terms_conditions,
        )
        user.is_admin = is_admin
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    User model.
    """
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    terms_conditions = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'terms_conditions']

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        """
        Returns whether user has specific permission.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Returns whether user can view the specified app.
        """
        return True

    @property
    def is_staff(self):
        """
        Return whether user is an admin.
        """
        return self.is_admin
