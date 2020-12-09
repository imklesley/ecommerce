from django.shortcuts import render
from .models import *
from django.http import HttpResponse


# Create your views here.


def store(request):
    context = {}
    products = Product.objects.all()

    context['products'] = products

    return render(request=request, template_name='store/store.html', context=context)


def cart(request):
    context = {}

    if request.user.is_authenticated:
        customer = request.user.customer
        # Status recebe Order.STATUS[0][0] pois no models falei que o campo seria um choice, logo criei
        # um valor para representar o estado da ordem [0][0] é o primeiro valor da tupla
        # ('In the cart', 'In the cart')
        orders, created = Order.objects.get_or_create(customer=customer, status=Order.STATUS[0][0])
        items = orders.orderitem_set.all()

    else:
        items = []

    context['items'] = items
    return render(request=request, template_name='store/cart.html', context=context)


def checkout(request):
    context = {}
    return render(request=request, template_name='store/checkout.html', context=context)
