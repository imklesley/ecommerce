let btnUpdateCart = document.getElementsByClassName('update-cart')

for (let i = 0; i <= btnUpdateCart.length; i++) {
    btnUpdateCart[i].addEventListener('click', function () {
        let productId = this.dataset.product;
        let action = this.dataset.action;

        if (user === 'AnonymousUser') {
            console.log('User not logged in!')
        } else {

            updateUserOrder(productId, action)

        }

    });
}


function updateUserOrder(productId, action) {
    console.log('The user ', user, 'clicked in the product with id:', productId, ' and the action is: ', action)
}

