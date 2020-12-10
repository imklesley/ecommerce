var btnUpdateCart = document.getElementsByClassName('update-cart')

for (var i = 0; i <= btnUpdateCart.length; i++) {
    btnUpdateCart[i].addEventListener('click', function () {

        var productId = this.dataset.product;
        var action = this.dataset.action;

        if (user === 'AnonymousUser') {
            console.log('User not logged in!!!  ');
            document.getElementById('error-add-cart').classList.remove('hidden');


        } else {

            console.log(productId, action)
            updateUserOrder(productId, action)

        }

    });
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

