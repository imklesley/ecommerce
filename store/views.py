from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout

import json
from datetime import datetime


def log_out(request):
    logout(request)
    return redirect('store')


def store(request):
    context = {}
    products = Product.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=Order.STATUS[0][0])

    else:
        order = {'get_total_order': 0, 'get_total_cart_items': 0}

    context['products'] = products

    context['order'] = order

    return render(request=request, template_name='store/store.html', context=context)


def cart(request):
    context = {}

    if request.user.is_authenticated:
        customer = request.user.customer
        # Status recebe Order.STATUS[0][0] pois no models falei que o campo seria um choice, logo criei
        # um valor para representar o estado da ordem [0][0] é o primeiro valor da tupla
        # ('In the cart', 'In the cart')
        order, created = Order.objects.get_or_create(customer=customer, status=Order.STATUS[0][0])
        items = order.orderitem_set.all()

    else:
        order = {'get_total_order': 0, 'get_total_cart_items': 0}
        items = []

    context['order'] = order
    context['items'] = items
    return render(request=request, template_name='store/cart.html', context=context)


def checkout(request):
    context = {}

    if request.user.is_authenticated:
        customer = request.user.customer
        # Status recebe Order.STATUS[0][0] pois no models falei que o campo seria um choice, logo criei
        # um valor para representar o estado da ordem [0][0] é o primeiro valor da tupla
        # ('In the cart', 'In the cart')
        order, created = Order.objects.get_or_create(customer=customer, status=Order.STATUS[0][0])
        items = order.orderitem_set.all()



    else:
        order = {'get_total_cart_items': 0, 'get_total_order': '0,00'}
        items = []

    context['order'] = order
    context['items'] = items
    return render(request=request, template_name='store/checkout.html', context=context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, status=Order.STATUS[0][0])
    if action == 'clear_cart':
        order.delete()
        return JsonResponse(f'Cart was cleared', safe=False)

    product = Product.objects.get(id=product_id)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'subtract':
        order_item.quantity -= 1
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse(f'Item was {action}ed', safe=False)


def process_order(request):
    data = json.loads(request.body)
    user_data = data['userData']
    shipping_data = data['shippingData']

    name = ''
    email = ''


    if user_data['name']:
        name = user_data['name']
        email = user_data['email']
    else:
        name = request.user.customer.name
        email = request.user.customer.email


    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=Order.STATUS[0][0])

        transaction_id = f'{name.replace(" ", "")}{datetime.now().timestamp()}'
        order.transaction_id = transaction_id


        order_item = order.orderitem_set.all()
        total = float(user_data['total'])

        if total == order.get_total_order:
            print('aqui2')

            order.status = Order.STATUS[2][0]
            for item in order_item:
                print(item)
                product = Product.objects.get(id=item.product.id)
                product.available_quantity -= item.quantity
                product.save()

        order.save()

        if order.shipping:
            ShippingAdress.objects.create(
                customer=customer,
                order=order,
                adress=shipping_data['address'],
                state=shipping_data['state'],
                city=shipping_data['city'],
                country=shipping_data['country'],
                zipcode=shipping_data['zipcode'],
                #     date_added é adicoinado automaticamente(auto_now_add=True)
            )



    else:
        print('user not logged in')

    return JsonResponse('Payment Completed', safe=False)
