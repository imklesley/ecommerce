from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Verifica se o usuário logou, caso não tenha logado redireciona para a página de login
from django.contrib.auth.decorators import login_required

##
from .forms import *
from .decorators import *

from store.utils import cartData
from store.models import Customer
from django.contrib.auth.models import User



@unauthenticated_user
def register_page(request):
    context = {}
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Ao salvar o formulário, salvo o user criado
            user = form.save()
            # Pego o user name do user, isso para mandar mensagem mais bonitinha para login_page
            username = form.cleaned_data.get('username')
            customer = Customer.objects.create(
                user=user,
                name=form.cleaned_data['first_name'],
                email=user.email,
            )
            customer.save()





            # Envia a mensagem de sucesso para a próxima page
            messages.success(request, message=f'{username} created with success !')
            return redirect('login_page')

    context['form'] = form
    return render(request, 'accounts/register_page.html', context)


@unauthenticated_user
def login_page(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request=request, message='Your username or password is invalid!')

    return render(request, 'accounts/login_page.html', context)




@login_required(login_url='login_page')
def user_orders(request):
    context = {}
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    waiting_payment = orders.filter(status='Waiting for Payment').count()
    preparation = orders.filter(status='Preparation').count()
    delivered = orders.filter(status='Delivered').count()

    data = cartData(request)

    context['order'] = {'get_total_cart_items':data['order'].get_total_cart_items}
    context['orders'] = orders
    context['total_orders'] = total_orders
    context['waiting_payment'] = waiting_payment
    context['preparation'] = preparation
    context['delivered'] = delivered

    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login_page')
def account_settings(request):
    context = {}
    customer = request.user.customer
    form = AccountSettingsForm(instance=customer)

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, message=f'{request.user.customer.name} Seu Perfíl Foi Atualizado!')
            return redirect('account_settings')


    data = cartData(request)

    context['order'] = {'get_total_cart_items': data['order'].get_total_cart_items}
    context['form'] = form

    return render(request=request, template_name='accounts/account_settings.html', context=context)


def log_out(request):
    logout(request)
    return redirect('store')