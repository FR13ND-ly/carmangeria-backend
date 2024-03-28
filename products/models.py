from django.db import models
from django.utils import timezone

class Product(models.Model):
    title = models.TextField()
    description = models.TextField()
    type = models.TextField()
    imageId = models.PositiveIntegerField(null=True)
    price = models.PositiveIntegerField(default = 0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title + " #" + str(self.id)


class Order(models.Model):
    name = models.TextField()
    phone = models.TextField()
    email = models.TextField(default = "")
    message = models.TextField(default = "")
    deliveryDate = models.DateField(default=timezone.now)
    completed = models.BooleanField(default = False)
    date = models.DateTimeField(default=timezone.now)


class OrderProduct(models.Model):
    orderId = models.PositiveIntegerField(null=True)
    productId = models.PositiveIntegerField(null=True)
    amount = models.PositiveIntegerField(null=True)
    price = models.PositiveIntegerField(null=True)


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.file.name
    
class Email(models.Model):
    email = models.EmailField()


class News(models.Model):
    text = models.TextField()