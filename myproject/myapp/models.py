from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import time

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('trader', 'Trader'),
        ('admin', 'Admin'),
        ('store', 'Store'),
        ('service_provider', 'ServiceProvider'),
    ]
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    membership = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email


class Trader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    trader_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    services = models.TextField()
    location = models.CharField(max_length=255)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE, null=True, blank=True)
    store = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()

class Service(models.Model):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_person = models.FloatField()
    max_capacity = models.IntegerField()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=50)  # e.g., pending, completed, failed
    created_at = models.DateTimeField(auto_now_add=True)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    appointment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    service = models.CharField(max_length=255)
    appointment_time = models.DateTimeField()
    num_persons = models.IntegerField(default=1)
    total_price = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class MilkDelivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    date = models.DateField()
    litres_delivered = models.FloatField()

class MonthlyBill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    month = models.DateField()
    total_litres = models.FloatField()
    total_price = models.FloatField()
    confirmed_by_customer = models.BooleanField(default=False)
    confirmed_by_trader = models.BooleanField(default=False)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profession = models.CharField(max_length=100)
    rating = models.FloatField(default=0)
    available_locations = models.ManyToManyField('Location', blank=True)  # New field for location-based availability

class Service(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_hour = models.FloatField()

class Availability(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_price = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)