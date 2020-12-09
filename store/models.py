from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    profile_img = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=300, null=False, blank=False)
    email = models.EmailField(max_length=300)
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
        #pego todos os itens de ordens
        orders_items = self.orderitem_set.all()
        #Faço um loop e somo todos valores de cada item
        total_order = sum(item.get_total_order_item for item in orders_items)
        return total_order

    @property
    def get_total_cart_items(self):
        #pego todos os itens de ordens
        orders_items = self.orderitem_set.all()
        #Faço um loop e somo todas as quantidade de cada item
        total_items = sum([item.quantity for item in orders_items])
        return total_items


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
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
    a = models.DateTimeField(auto_now_add=True)
    date_added = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.adress
