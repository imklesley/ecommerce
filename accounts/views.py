from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .decorators import *

from store.utils import cartData
from store.models import Customer
from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(self.request, 'accounts/register_page.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
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
            messages.success(request, message=f'{username} sua conta foi criada com sucesso!')
            return redirect('login_page')

class LoginView(View):
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login_page.html', self.context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request=request, message='Seu username ou senha são inválidos')

        return render(request, 'accounts/login_page.html', self.context)

# class UserOrders(LoginRequiredMixin, View):
class UserOrders(View):
    login_url = 'login_page'
    context = {}

    def get(self, request, *args, **kwargs):
        orders = request.user.customer.order_set.all()
        total_orders = orders.count()
        waiting_payment = orders.filter(status='Waiting for Payment').count()
        preparation = orders.filter(status='Preparation').count()
        delivered = orders.filter(status='Delivered').count()

        data = cartData(request)

        self.context['order'] = {'get_total_cart_items': data['order'].get_total_cart_items}
        self.context['orders'] = orders
        self.context['total_orders'] = total_orders
        self.context['waiting_payment'] = waiting_payment
        self.context['preparation'] = preparation
        self.context['delivered'] = delivered

        return render(request, 'accounts/my_orders.html', self.context)

class AccountSettingsView(View):
    context = {}
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        customer = request.user.customer
        form = AccountSettingsForm(instance=customer)
        data = cartData(request)

        self.context['order'] = {'get_total_cart_items': data['order'].get_total_cart_items}
        self.context['form'] = form

        return render(request=request, template_name='accounts/account_settings.html', context=self.context)

    def post(self, request, *args, **kwargs):
        form = AccountSettingsForm(request.POST, request.FILES, instance=self.request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request, message=f'{request.user.customer.name} Seu Perfíl Foi Atualizado!')
            return redirect('account_settings')


class LogoutView(View):
    login_url = 'login_page'

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('store')