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
    

@admin.register(RegisterModel)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('name','lastname','email','password','phone')
    list_editable = ('lastname','email','phone',)
    list_filter = ('name','lastname')
    search_fields = ('name','lastname','phone')
    ordering = ('name','lastname')
    list_per_page = 50 


    

        
