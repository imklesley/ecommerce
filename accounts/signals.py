# Pra adicionar o group de permisão do usuário quando ele está sendo  criado
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer


def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        if group:
            instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )

        print('Profile Created!!')

post_save.connect(customer_profile, sender=User)





"""
        SIGNALS
Signals são formas de realizar operações baseadas em gatilhos, é criado um signal que avisa
uma outra função que ela deve ser executada. O exemplo criado é o de configurar um usuário após
sua criação como do tipo customer, e do group de permissão customer

PASSOS PARA CRIAR UM SIGNAL:

0 - Importar todas as classe necessárias. No caso User, Customer e Group

1- criar a função que irá ser chamada após algo acontecer, no caso que vai dar o sinal é a classe User.
    1.1 Nesse exemplo nome da função é customer_profile. 
    1.2 É obrigatório colocar os parametros: (sender, instance, created, **kwargs)
    1.3 É preciso fazer a verificação "if created:" se true, realizasse o que deseja, no caso adicionar um group de permissão e criar um customer para o user criado

2 - Usar a função, previamente importada, post_save, e fazer o "connect" entre a função criada e a classe que vai mandar o signal, no caso a sender
    post_save.connect(função_criada,sender=ClasseQueMandaSignal)
    No nosso exemplo:
        post_save.connect(create_profile,sender=User)

3 - Configurar, no arquivo settings, nome dos apps. NÃO PODE SER O NOME SIMPLIFICADO. "accounts" vira "accounts.app.AccountsConfig"(Esse é o caminho do arquivo de config desse app especificamente)

4 - Dentro do arquivo apps.py do app em questão, devesse dar um override na função ready(self): dando um import no arquivo signals criados:
      
    class AccountsConfig(AppConfig):
        name = 'accounts'

        def ready(self):
            import accounts.signals


5 - roda esse carai e testa

"""