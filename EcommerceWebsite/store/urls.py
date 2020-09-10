from django.urls import path
from . import views # 從當前目錄引用views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('updateitem/', views.updateItem, name='updateitem'), # 這頁面是處理加入購物車使用，本身只在後端使用
    path('processorder/', views.processOrder, name="processorder"), # 處理訂單
    path('view/<str:ProductId>', views.ProductDetailView.as_view(), name="view"), # 處理訂單
]