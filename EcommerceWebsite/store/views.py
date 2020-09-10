from django.shortcuts import render
from.models import * # 引入model類別
from django.http import JsonResponse # update view使用 把資料用json格式回傳
import json
import datetime
from .utils import cookieCart, cartData, guestOrder # 從utils引入function
from django.core.paginator import Paginator # 分頁
from accounts.models import *
from django.views.generic import DetailView # 顯示明細資訊
from django.shortcuts import render, get_object_or_404

# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    order_items = data['items']
    products = Product.objects.all() # 顯示在頁面上的商品
    paginator = Paginator(products, 6)  # Show 6 products per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products, 'cartItems':cartItems, 'page_obj': page_obj}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    order_items = data['items']

    context = {'order_items': order_items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    order_items = data['items']

    context = {'order_items': order_items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data['quantity']

    print('Action:', action)
    print('Product:', productId)
    print('Quantity:', quantity)

    user = User.objects.get(email=request.user)  # 先找到使用者，因為customer是一對一關係
    if not Customer.objects.filter(user=request.user).exists(): # user 尚未變成customer，所以新增，不然後續無法作業
        Customer.objects.create(user=user, name=request.user.name, email=request.user.email)

    customer = Customer.objects.get(user=user)
    product = Product.objects.get(id=productId)
    transaction_id = '{}_{}'.format(request.user, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + quantity)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - quantity)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = '{}_{}'.format(request.user, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = User.objects.get(email=request.user)
        customer = Customer.objects.get(user=user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
       customer, order = guestOrder(request, data)
    total = data['form']['total']
    if int(total) == order.get_cart_total:
        order.transaction_id = transaction_id
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address']
        )

    return JsonResponse('Payment submitted..', safe=False)

class ProductDetailView(DetailView): # 顯示account的profile
    template_name = 'store/view.html'
    queryset = Product.objects.all()

    def get_object(self):
        product_id = self.kwargs.get("ProductId")
        return get_object_or_404(Product, id=product_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = cartData(self.request)
        cartItems = data['cartItems']
        context['cartItems'] = data['cartItems']
        return context



def view(request): # 商品內頁
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    order_items = data['items']

    context = {'order_items': order_items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/view.html', context)