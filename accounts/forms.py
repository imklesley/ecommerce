from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# O model do usuário já é criado pelo Django, logo basta importarmos
from django.contrib.auth.models import User
from store.models import *




class OrderForm(ModelForm):
    class Meta:
        model = Order
        # Vai criar um form na qual todos os campos do model Order está presente, caso fossem somente alguns field seria ['campo1', 'campo2']
        fields = '__all__'


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','email', 'password1', 'password2']


class AccountSettingsForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']