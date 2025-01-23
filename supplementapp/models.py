from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now

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
    description = models.CharField(max_length=100)  # 'descriptions' to 'description'
    image = models.ImageField(upload_to='products/images/')  # Specify upload path

    def __str__(self):
        return self.name




class RegisterModel(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    lastname = models.CharField(max_length=40, blank=False, null=False)
    email = models.EmailField(unique=True,blank=True, null=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    phone_validator = RegexValidator(regex=r'^09\d{9}$', message="Phone number must start with '09' and be 11 digits long.")
    phone = models.CharField(max_length=11, blank=False, validators=[phone_validator])
    last_login = models.DateTimeField(default=now, blank=True, null=True)


    def __str__(self):
        return self.name
    
