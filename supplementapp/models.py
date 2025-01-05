from django.db import models



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
