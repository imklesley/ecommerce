var btnUpdateCart = document.getElementsByClassName('update-cart')

for (var i = 0; i <= btnUpdateCart.length; i++) {
    btnUpdateCart[i].addEventListener('click', function (event) {
        event.preventDefault();

        var productId = this.dataset.product;
        var action = this.dataset.action;

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            console.log(productId, action)
            updateUserOrder(productId, action);
        }
    });
}


function addCookieItem(productId, action) {
    console.log('User not logged in!!!!!!');
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1};
        } else {
            cart[productId]['quantity'] += 1;
        }
    } else if (action == 'subtract') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
            console.log('Item deleted');

        }
    } else if (action == 'clear_cart') {
        cart = {}
        console.log('Cart was cleaned!');

    }

    console.log('Cart: ', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();


}


function updateUserOrder(productId, action) {
    console.log('The user ', user, 'clicked in the product with id:', productId, ' and the action is: ', action, 'Sending data')

    var url = '/update_item/'

    //Para enviar o nosso post data
    fetch(url, {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

        .then(function (response) {
            return response.json()
        })

        .then((data) => {
            console.log('response from backend: ', data)
            location.reload()
        }).catch(function (error) {
        console.error(error)
    })


}

