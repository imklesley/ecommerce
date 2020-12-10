from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse

import json


# Create your views here.


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
        context['order'] = order
        context['items'] = items

    else:
        return HttpResponse('You is not authorized!!')

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
