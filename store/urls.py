from django.urls import path
from .views import *



urlpatterns = [
    path('', StoreView.as_view(), name='store'),
    path('product_details/<str:pk>', ProductDetailsView.as_view(), name='product_details'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('update_item/', update_item, name='update_item'),
    path('process_order/', process_order, name='process_order'),

]
