from django.db import models
from django.conf import settings # 使用自建的user model
User = settings.AUTH_USER_MODEL # 使用自建的user model
from django.conf import settings
import re
import os
from django.dispatch import receiver # 刪除圖片
from django.contrib import admin

def product_image_filename(instance, filename): # uploadto會給instance跟filename
    # file will be uploaded to MEDIA_ROOT/product.id.file_type
    file_type = re.findall(r'\.(.*)',filename) # 用正規表達式找出jpg or png
    file_name = 'ProductImages/{}.{}'.format(instance.id, file_type[0])
    fullpath = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(fullpath): # 更新照片時，可以砍掉原本的照片。因為我要一個產品只能一張照片，不希望變得太多張。
        print('remove old version')
        os.remove(fullpath)
    return file_name

# Create your models here.

class Customer(models.Model): # 消費者跟User未必是等號，你可以是user但未必要消費
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)# Foreignkey: User
    name = models.CharField(max_length=200, null = True)
    email = models.EmailField(max_length=254, null = True) # EmailField會自動驗證是否為email格式

    def __str__(self):
        return str(self.user)


class Product(models.Model):
    id = models.CharField(max_length=200, null=False, primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=100000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to =product_image_filename) # 為了不要無限擴充圖片資料夾，一個產品只配一張圖片，用產品id進行命名。

    def __str__(self):
        return "{}".format(self.id)

    @property
    def imageURL(self): # 如果沒有圖片，就返回空值
        try:
            url = self.image.url
        except:
            url = ''
        return url

@receiver(models.signals.post_delete, sender=Product) # 刪除圖片用的
def delete_ExampleImageModel_images(sender, instance, **kwargs):
    """
    Deletes ExampleImageModel image renditions on post_delete.
    """
    # Deletes Image Renditions
    # instance.image.delete_all_created_images()
    # Deletes Original Image
    instance.image.delete(save=False)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) # Foreignkey: Customer
    date_ordered = models.DateTimeField(auto_now_add=True) # 下單時自動新增
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.transaction_id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all() # 這邊不懂
        total =sum([item.calculate_total for item in orderitems]) # 這寫法很酷
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])  # 這寫法很酷
        return total

    @property
    def shipping(self): # 我要所有東西都用寄送的
        shipping = True
        return shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) # Foreignkey: product
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) # Foreignkey: Order
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self): # 這邊要再考慮一下，是不是transaction_id，比較合適
        return "{}_{}".format(self.order, self.product)

    @property
    def calculate_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) # Foreignkey: Customer
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)  # Foreignkey: Order
    address = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)

