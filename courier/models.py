from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# class CompanyUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field is required")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')

#         return self.create_user(email, password, **extra_fields)



class CompanyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # overridden to store raw password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)
# class Signup(AbstractBaseUser, PermissionsMixin):
#     company_name = models.CharField(max_length=50)
#     address = models.CharField(max_length=100)
#     ownername = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     contact = models.CharField(max_length=15)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['company_name', 'ownername']

#     objects = CompanyUserManager()

#     def __str__(self):
#         return self.ownername

#     class Meta:
#         db_table = 'signup'


class Signup(AbstractBaseUser, PermissionsMixin):
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    ownername = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # override password field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'ownername']

    objects = CompanyUserManager()

    def set_password(self, raw_password):
        # Override to save raw password instead of hashing
        self.password = raw_password

    def check_password(self, raw_password):
        # Compare directly
        return self.password == raw_password

    def __str__(self):
        return self.ownername

    class Meta:
        db_table = 'signup'
