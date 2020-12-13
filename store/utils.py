from .models import Product, Order, Customer, OrderItem
import json


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    total_cart_items = 0
    total_order = 0
    items = []
    shipping = False

    for product_id in cart:
        try:
            quantity = cart[product_id]['quantity']
            product = Product.objects.get(id=product_id)
            items.append(
                {'product': product, 'quantity': quantity, 'get_total_order_item': product.price * quantity})

            total_cart_items += quantity
            total_order += product.price * quantity

            if product.digital == False:
                shipping = True

        except:
            pass

    quantity_items = total_cart_items

    order = {'get_total_order': total_order, 'get_total_cart_items': total_cart_items, 'shipping': shipping}

    return {'order': order, 'items': items, 'quantity_items': quantity_items}


def cartData(request) -> dict:
    """
    Verifica se o usuário está logado e qual tipo de informação deve retornar. Caso não esteja logado, realizaa lógica nos cookies e retorna pro usuário.
    :param request:
    :return:
    """

    if request.user.is_authenticated:
        customer = request.user.customer
        # Status recebe Order.STATUS[0][0] pois no models falei que o campo seria um choice, logo criei
        # um valor para representar o estado da ordem [0][0] é o primeiro valor da tupla
        # ('In the cart', 'In the cart')
        order, created = Order.objects.get_or_create(customer=customer, status=Order.STATUS[0][0])
        items = order.orderitem_set.all()
        quantity_items = items.count()
        return {'order': order, 'items': items, 'quantity_items': quantity_items}
    else:

        return cookieCart(request)


def guestOrder(request, user_data):
    name = user_data['name']
    email = user_data['email']
    # print(name)
    # print(email)
    cookie_cart = cookieCart(request)

    items = cookie_cart['items']

    customer, created = Customer.objects.get_or_create(email=email)
    #Se o usuário já possui um nome, então ele já foi criado uma veze não precisa sofrer override
    if customer.name == None:
        customer.name = name
    customer.save()
    order = Order.objects.create(customer=customer, status=Order.STATUS[0][0])

    for item in items:
        product = Product.objects.get(id=item['product'].id)
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
        order_item.save()

    return customer, order
