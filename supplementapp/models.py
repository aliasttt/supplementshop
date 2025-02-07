from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now
import datetime
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render , HttpResponse ,redirect
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class ProductModel(models.Model):
    CATEGORY_CHOICES = [
        ('whey', 'Whey'),
        ('casein', 'Casein'),
        ('isolate', 'Isolate'),
        ('mass_gainer', 'Mass Gainer'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='whey'
    )
    name = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=100) 
    created_at = models.DateTimeField(default=timezone.now)  # Set on object creation
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/images/')  

    def __str__(self):
        return self.name



    






phone_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message="Phone number must start with '09' and be 11 digits long."
)

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("The Phone number must be set")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone, password, **extra_fields)

class RegisterModel(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=20)
    lastname = models.CharField(max_length=40)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True, validators=[phone_validator])
    last_login = models.DateTimeField(default=now, blank=True, null=True)
    
    # فیلدهای ضروری برای مدیریت
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone'           # فیلد شناسه‌ی کاربری
    REQUIRED_FIELDS = ['name', 'lastname']  # فیلدهایی که هنگام ساخت سوپر یوزر نیاز است
    # این دوتا بالایی برای رجیستر مدل اجبار بود که صفحه ثبتانم وقتی تو دیتا بیس ذخیره شد بعنوان یوزر تو سشن شناسایی بشه



    objects = CustomUserManager()

    def __str__(self):
        return self.phone



class Basket(models.Model):
    user = models.OneToOneField(RegisterModel, on_delete=models.CASCADE, related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"سبد خرید {self.user.name}"

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.name} در سبد {self.basket.user.name}"

    
