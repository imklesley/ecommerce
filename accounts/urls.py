from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login_page/', views.login_page, name='login_page'),
    path('register_page/', views.register_page, name='register_page'),
    path('logout/', views.log_out, name='logout'),
    path('my_orders/', views.user_orders, name='my_orders'),
    path('account_settings/', views.account_settings, name='account_settings'),



]
