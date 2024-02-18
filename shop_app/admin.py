from django.contrib import admin
from shop_app.models import Category, Product, Order, Cart
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','image','category','qty','price','created_at']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Cart)

