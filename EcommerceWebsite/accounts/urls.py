from django.urls import path
from . import views # 從當前目錄引用views

from django.conf import settings # 為了上傳圖片
from django.conf.urls.static import static # 為了上傳圖片

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('profile/<str:email>', views.UserDetailView.as_view(), name='profile'),  # profile # <str:email> 傳參數
    path('profile/<str:email>/update', views.UserUpdateView.as_view(), name='update'),
    path('profile/<str:email>/delete', views.UserDeleteView.as_view(), name='delete'),
]