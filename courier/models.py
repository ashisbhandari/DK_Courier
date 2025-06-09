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




class Booking_list(models.Model):
    cn_no = models.CharField(max_length=20, unique=True, blank=True)


    # Country & District
    country = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)

    # Packet Info
    pactype = models.CharField(max_length=50)
    date = models.DateField()

    # Sender Details
    Sname = models.CharField(max_length=100)
    Snumber = models.CharField(max_length=10)
    Saddress = models.CharField(max_length=255)
    Saddress1 = models.CharField(max_length=255, blank=True, null=True)

    # Receiver Details
    Rname = models.CharField(max_length=100)
    Rnumber = models.CharField(max_length=10)
    Raddress = models.CharField(max_length=255)
    Raddress1 = models.CharField(max_length=255, blank=True, null=True)

    # Package & Payment Info
    payments = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Credit', 'Credit'), ('COD', 'COD')])
    service = models.CharField(max_length=50, choices=[('Door to Door', 'Door to Door'), ('Office Collect', 'Office Collect')])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.FloatField()
    pieces = models.PositiveIntegerField()
    Bookby = models.CharField(max_length=100)
    
    class Meta:
        db_table = "Booking_list"
    
    def save(self, *args, **kwargs):
        if not self.cn_no:
            last_booking = Booking_list.objects.order_by('-id').first()
            if last_booking and last_booking.cn_no:
                last_number = int(last_booking.cn_no.replace('DK170', ''))
                new_number = last_number + 1
            else:
                new_number = 1
            self.cn_no = f'DK170{new_number:03}'
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.cn_no} to {self.country} ({self.Rname})"


class BookingForm(models.Model):
    cn_no = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    pactype = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    
    Sname = models.CharField(max_length=100)
    Snumber = models.CharField(max_length=10)
    Saddress = models.CharField(max_length=200)
    Saddress1 = models.CharField(max_length=200, blank=True, null=True)
    
    Rname = models.CharField(max_length=100)
    Rnumber = models.CharField(max_length=10)
    Raddress = models.CharField(max_length=200)
    Raddress1 = models.CharField(max_length=200, blank=True, null=True)
    
    payments = models.CharField(max_length=20)
    service = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    pieces = models.IntegerField()
    Bookby = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.cn_no

class BookingList(models.Model):
    cn_no = models.CharField(max_length=100)
    date = models.DateField()
    sname = models.CharField(max_length=100)
    snumber = models.CharField(max_length=20)
    pactype = models.CharField(max_length=100)
    pieces = models.IntegerField()
    rname = models.CharField(max_length=100)
    raddress = models.TextField()
    rnumber = models.CharField(max_length=20)
    service = models.CharField(max_length=100)
    # Remarks = models.TextField()

    class Meta:
        db_table = 'booking_list'
        managed = False  # since you're using an existing table
