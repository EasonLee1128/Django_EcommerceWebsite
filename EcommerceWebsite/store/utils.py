import json
from .models import *
from accounts.models import *

def cookieCart(request):
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    order_items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            print(total)

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'id': product.id,
                'product': {'id': product.id, 'name': product.name, 'price': product.price,
                            'imageURL': product.imageURL}, 'quantity': cart[i]['quantity'], 'calculate_total': total}
            order_items.append(item)

        except:
            pass
        print(order_items)

    return {'cartItems': cartItems, 'order': order, 'items': order_items}

def cartData(request):
    if request.user.is_authenticated:
        try: # 當尚未是customer時會當機
            user = User.objects.get(email=request.user)
            customer = Customer.objects.get(user=user)
            Order.objects.filter(customer=None).delete() # 找到一開始創造出來的delete
        except:
            customer = None
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all() # 訂單的所有品項
        cartItems = order.get_cart_items # 算出有幾件品項
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        order_items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': order_items}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(user=User.objects.get(name='AnonymousUser'),name=name,email=email)
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
        )

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order
