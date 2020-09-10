from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView # 新增、修改、刪除
from django.views.generic import DetailView # 顯示使用者明細資訊
from .models import User
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate # login
from django.contrib.auth import login as auth_login # login
from django.contrib.auth import logout as auth_logout # logout
from django.shortcuts import redirect # login使用
from django.contrib import messages # login使用
from store.utils import cookieCart, cartData, guestOrder # 引入function

# Create your views here.

def logout(request):
    auth_logout(request)
    return redirect('store')

def login(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Redirect to a success page.
            auth_login(request, user)
            return redirect('store')
        else:
            # Return an 'invalid login' error message.
            messages.info(request, 'E-mail or Password not correct')
    context = {}
    return render(request, './login.html', context)

class UserRegister(CreateView): # 註冊
    model = User # 使用的model
    form_class = RegisterForm # 使用的form，這邊直接參照form那邊要的field
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        cartItems = data['cartItems']
        context['cartItems'] = data['cartItems']
        return context

class UserDetailView(DetailView): # 顯示profile
    template_name = 'profile.html'
    queryset = User.objects.all()

    def get_object(self):
        email_ = self.kwargs.get("email")
        return get_object_or_404(User, email=email_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        cartItems = data['cartItems']
        context['cartItems'] = data['cartItems']
        return context

class UserUpdateView(UpdateView): # 更新會員資料
    model = User # 使用的model
    fields = ['password', 'name', 'gender', 'city', 'date_of_birth', 'image'] # 全部都開放更改
    queryset = User.objects.all()
    template_name = 'update.html'

    def get_object(self):
        email_ = self.kwargs.get("email")
        return get_object_or_404(User, email=email_)

class UserDeleteView(DeleteView): # 刪除會員資料
    template_name = 'delete.html'
    success_url = reverse_lazy('store')

    def get_object(self): # 用account去找資料
        email_ = self.kwargs.get("email")
        instance = get_object_or_404(User, email=email_)
        return instance.delete()