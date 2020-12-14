from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login_page/', views.LoginView.as_view(), name='login_page'),
    path('register_page/', views.RegisterView.as_view(), name='register_page'),
    path('my_orders/', views.UserOrders.as_view(), name='my_orders'),
    path('account_settings/', views.AccountSettingsView.as_view(), name='account_settings'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # https://docs.djangoproject.com/en/3.0/topics/auth/default/#all-authentication-views
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html', ),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    # Para configurar o gmail para enviar mensagens seguir:
    # https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab
    #Caso seguindo os passos anteriores não funcionarem desativar aqui:
    #https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4MVA_IyNi69Hd3GOmh69schMKZSlIwbdlzq9nY4s5bncIUq5HC-vz7C6a2EUlI5YtI1ky2GpWPCxs0dybuALhlqZbFODQ
]
