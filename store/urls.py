from django.urls import path
from .views import *



urlpatterns = [
    path('', StoreView.as_view(), name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', update_item, name='update_item'),
    path('process_order/', process_order, name='process_order'),
    path('logout/', log_out, name='logout'),

]
