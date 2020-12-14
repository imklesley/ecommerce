from .models import *
from django.http import JsonResponse
from .utils import *
import json
from datetime import datetime

# class-based view
from django.views.generic import ListView, DetailView, View


class StoreView(ListView):
    # Dados que seão exibidos
    model = Product
    # nome desse model chamado no html, caso não coloque será object_list
    context_object_name = 'products'
    # É preciso sobrescrever o template
    template_name = 'store/store.html'

    # Para realizar paginação basta fazer isso.COISA MAIS LINDA QUE JÁ Ví kkk
    paginate_by = 9

    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super(StoreView, self).get_context_data(**kwargs)
        data = cartData(self.request)
        order = data['order']
        # print(order)
        context['order'] = order
        return context


class ProductDetailsView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/product_details.html'
    queryset = Product.objects.all()

    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ProductDetailsView, self).get_context_data(**kwargs)
        data = cartData(self.request)
        order = data['order']
        context['order'] = order
        return context


class CartView(ListView):
    # Dados que seão exibidos
    model = Product
    # nome desse model chamado no html, caso não coloque será object_list
    context_object_name = 'products'
    # É preciso sobrescrever o template
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        data = cartData(self.request)
        order = data['order']
        # print(order)
        context['order'] = order
        context['quantity_items'] = data['quantity_items']
        context['items'] = data['items']
        return context


class CheckoutView(ListView):
    # Dados que seão exibidos
    model = Product
    # nome desse model chamado no html, caso não coloque será object_list
    context_object_name = 'products'
    # É preciso sobrescrever o template
    template_name = 'store/checkout.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        data = cartData(self.request)
        order = data['order']
        # print(order)
        context['order'] = order
        context['quantity_items'] = data['quantity_items']
        context['items'] = data['items']
        return context


class UpdateItemCartView(View):

    def post(self, request, *args, **kwargs):
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


#    {#LEMBRE QUE A OPÇÃO PAY WITH DEBIT OR CREDIT CARD SÓ IRÁ APARECER SE O SITE EM PRODUÇÃO POSSUIR certificado ssl#}
class ProcessOrderView(View):

    def post(self, request, *args, **kwargs):
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
