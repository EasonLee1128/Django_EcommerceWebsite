from django.db import models
from django.contrib.auth.models import PermissionsMixin# 許可權力設置
from django.contrib.auth.base_user import AbstractBaseUser # 原生user moder
import django.utils.timezone as timezone # 新增當下的時間
import re # 正規表示法
from django.contrib.auth.models import UserManager
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
import re
import os


def user_image_filename(instance, filename): # uploadto會給instance跟filename
    # file will be uploaded to MEDIA_ROOT/product.id.file_type
    file_type = re.findall(r'\.(.*)',filename) # 用正規表達式找出jpg or png
    file_name = 'UserImages/{}.{}'.format(instance.id, file_type[0])
    fullpath = os.path.join(settings.MEDIA_ROOT, file_name)
    print(fullpath)
    if os.path.exists(fullpath): # 更新照片時，可以砍掉原本的照片。因為我要一個產品只能一張照片，不希望變得太多張。
        print('Delete old')
        os.remove(fullpath)
    return file_name


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser ,PermissionsMixin):
    name = models.CharField(max_length=20, null=False)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    gender_items = (('Man', 'Man'), ('Women',"Women"))
    gender = models.CharField(choices=gender_items,max_length=20, default='Man') # 使用選擇器

    city_items = (('New Taipei', 'New Taipei'), ('Taipei', 'taipei'), ('Yilan', 'Yilan'),
                  ('Taoyuan', 'Taoyuan'), ('Hsinchu', 'Hsinchu'), ('Miaoli', 'Miaoli'),
                  ('Taichung', 'Taichung'), ('Changhua', 'Changhua'), ('Nantou', 'Nantou'),
                  ('Yunlin', 'Yunlin'), ('Chiayi', 'Chiayi'), ('Tainan', 'Tainan'),
                  ('Kaohsiung', 'Kaohsiung'), ('Pingtung', 'Pingtung'), ('Taitung', 'Taitung'),
                  ('Hualien', 'Hualien'), ('Penghu', 'Penghu'), ('Kinmen', 'Kinmen'),
                  ('Lienchiang', 'Lienchiang'))
    city = models.CharField(choices=city_items,max_length=20, null=False) # 使用選擇器

    date_of_birth = models.DateField(null=False, default=timezone.now)
    image = models.ImageField(null=True, upload_to=user_image_filename)  # 上傳圖片
    registration_date = models.DateTimeField(auto_now_add=True) # 註冊的時間: 自動現在的時間
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager() # 指定管理員
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self): # admin頁面顯示的名字。
        return self.email

    def has_perm(self, perm, obj=None): # 權限
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label): # 權限
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_absolute_url(self): # 這邊是存完後的網址，還沒設定。
        from django.urls import reverse
        # return reverse('store', kwargs={"email": str(self.email)}) # 去url.py那邊看ID拿網址
        return reverse('store')  # 去url.py那邊看ID拿網址