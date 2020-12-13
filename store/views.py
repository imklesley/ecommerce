from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from .utils import *

import json
from datetime import datetime


def log_out(request):
    logout(request)
    return redirect('store')


def store(request):
    context = {}

    data = cartData(request)

    products = Product.objects.all()

    order = data['order']

    context['products'] = products

    context['order'] = order

    return render(request=request, template_name='store/store.html', context=context)


def cart(request):
    context = {}

    data = cartData(request)

    context['order'] = data['order']
    context['items'] = data['items']
    context['quantity_items'] = data['quantity_items']
    return render(request=request, template_name='store/cart.html', context=context)


def checkout(request):
    context = {}
    data = cartData(request)
    if data['quantity_items'] == 0:
        return HttpResponse("You are not authorized to access this page!")

    context['order'] = data['order']
    context['items'] = data['items']
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


def process_whatsapp_order(request):
    return JsonResponse('Whats Message Ready To Send', safe=False)




#    {#LEMBRE QUE A OPÇÃO PAY WITH DEBIT OR CREDIT CARD SÓ IRÁ APARECER SE O SITE EM PRODUÇÃO POSSUIR certificado ssl#}
def process_order(request):
    data = json.loads(request.body)
    # print(data)
    user_data = data['userData']
    shipping_data = data['shippingData']

    # Usuário com cadastro
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=Order.STATUS[0][0])

    # Usuário Visitante
    else:
        customer, order = guestOrder(request, user_data)

    # Finaliza o processo. Todas as condicionais possuem o mesmo fim
    transaction_id = f'{customer.name.replace(" ", "")}{datetime.now().timestamp()}'
    order.transaction_id = transaction_id

    order_item = order.orderitem_set.all()
    total = float(user_data['total'])

    if total == order.get_total_order:
        order.status = Order.STATUS[2][0]
        for item in order_item:
            # print(item)
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

    return JsonResponse('Payment Completed', safe=False)
