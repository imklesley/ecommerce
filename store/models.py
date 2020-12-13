from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_img = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=300, null=False, blank=False)
    email = models.EmailField(max_length=300, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    digital = models.BooleanField(default=False, null=False)
    available_quantity = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.name

    @property
    def image_url(self):

        try:
            url = self.image.url
        except:
            url = f'/static/images/Sem-imagem.png'

        return url


class Order(models.Model):
    STATUS = [
        ('In the cart', 'In the cart'),
        ('Waiting for Payment', 'Waiting for Payment'),
        ('Preparation', 'Preparation'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS, default=STATUS[0])
    transaction_id = models.CharField(max_length=200, null=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_order(self):
        # pego todos os itens de ordens
        orders_items = self.orderitem_set.all()
        # Faço um loop e somo todos valores de cada item
        total_order = sum(item.get_total_order_item for item in orders_items)
        return float(total_order)

    @property
    def get_total_cart_items(self):
        # pego todos os itens de ordens
        orders_items = self.orderitem_set.all()
        # Faço um loop e somo todas as quantidade de cada item
        total_items = sum([item.quantity for item in orders_items])
        return total_items

    @property
    def shipping(self):
        # Carrega-se todos os items do pedido
        items = self.orderitem_set.all()
        # Faço um loop para criar uma lista que contenha somente os valores do atributo "digital"
        type_products = [item.product.digital for item in items]
        # Verifico se dentro da lista de tipos de produtos existe algum que não seja digital(False)
        need_shipping = False in type_products
        # Retorno essa condicional.
        return need_shipping

    @property
    def whatsapp_order_text(self):
        #Código para pular linha
        break_line = '%0A'
        #pego todos os itens dentro do pedido
        items = self.orderitem_set.all()
        #Inicializo o texto a ser enviado pro cliente e adiciono duas vezes o break_line
        text = f'Olá, gostaria de fazer um pedido: {break_line}{break_line}'
        #Pra cada item da ordem especificar os detalhes e pular uma linha
        for item in items:
            text += f'*{item.quantity}x*\t-\t{item.product.name}\t-\t{item.product.price}{break_line}'

        text += break_line
        text += '-----------------------------' + break_line

        #Mostra os quantitativos
        text += f'*Quantidade de Itens:* {self.get_total_cart_items}{break_line}'
        text += f'*Total:* {self.get_total_order}{break_line}'

        return text

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total_order_item(self):
        return self.product.price * self.quantity


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    adress = models.CharField(max_length=300, null=False)
    state = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=100, null=False)
    zipcode = models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.adress
