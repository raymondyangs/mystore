import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='產品名稱')
    description = models.TextField(verbose_name='產品敘述')
    quantity = models.IntegerField(verbose_name='庫存數量')
    price = models.IntegerField(verbose_name='價格')
    image = models.ImageField(upload_to='product_images/', verbose_name='商品圖片', blank=True, null=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    items = models.ManyToManyField(Product)

    def total_price(self):
        sum = 0
        for product in self.items.all():
            sum += product.price
        return sum


class OrderInfo(models.Model):
    billing_name = models.CharField(max_length=255, verbose_name='購買人姓名')
    billing_address = models.CharField(max_length=255, verbose_name='購買人地址')
    shipping_name = models.CharField(max_length=255, verbose_name='收件人姓名')
    shipping_address = models.CharField(max_length=255, verbose_name='收件人地址')


class Order(models.Model):
    info = models.OneToOneField(OrderInfo, on_delete=models.CASCADE, primary_key=True, verbose_name='訂購資訊')
    total = models.IntegerField(default=0, verbose_name='總價')
    user = models.ForeignKey(User, verbose_name='訂購使用者', null=True, on_delete=models.SET_NULL)
    token = models.UUIDField(db_index=True, default=uuid.uuid4)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=255, default='')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='產品名稱')
    price = models.IntegerField(verbose_name='價格')
    quantity = models.IntegerField(verbose_name='數量')
