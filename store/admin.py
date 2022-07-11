from django.contrib import admin
from .models import Product
from .models import Category
from .models import Customer
from .models import Order
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','category']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','phone','email','password']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','product','customer','quantity','price','address','phone','date']
