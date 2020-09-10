from django.contrib import admin
from .models import *

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'name', 'email')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer','date_ordered', 'complete', 'transaction_id')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

