from django.contrib import admin
from .models import Product, Order, OrderProduct, File, Email

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(File)
admin.site.register(Email)