from django.contrib import admin
from .models import Product, Order, OrderProduct, File, Email, News

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(File)
admin.site.register(Email)
admin.site.register(News)