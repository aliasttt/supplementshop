from django.contrib import admin
from .models import *


@admin.register(ProductModel)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','image')
    list_editable = ('category','price','image')
    list_filter = ('category','price')
    search_fields = ('name', 'category')
    ordering = ('price',)
    list_per_page = 50 
    

    

        
