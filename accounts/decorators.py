from django.shortcuts import redirect
from django.http import HttpResponse

##Nesse arquivo irá ficar os decorators, decorators nada mais são que funções que recebem outra função como parâmetro

"""Essa verifica se o usuário está autenticado"""


def unauthenticated_user(view):
    # wrapper_func é o nome da nossa função enviada por parâmetro, no caso nossa view
    def wrapper_func(request, *args, **kwargs):
        # Se o usuário está autenticado, ele não precisa vê a página de login e/ou register
        if request.user.is_authenticated:
            return redirect('home')
        # Caso contrário permite o acesso à página de login e/ou register
        else:
            return view(request, *args, **kwargs)

    # Retorna o que foi decidido na wrapper_func
    return wrapper_func


#Somente os grupos de usuário podem acessar determinada view
def allowed_users(allowed_roles=None):

    #Caso "allowed_roles" continue None significa que não foi passado nenhum regra, logo criamos uma lista vazia
    if allowed_roles is None:
        allowed_roles = []

    #A função que vai carregar nossa view
    def decorator(view):
        #Função que irá fazer pré-operações na nossa view
        def wrapper_func(request, *args, **kwargs):
            #Inicialização da var group
            group = None

            # Esse usuário está em algum grupo de permissão?
            if request.user.groups.exists():
                #Se sim, pega o nome do primeiro dessa lista
                group = request.user.groups.all()[0].name

                #O grupo escolhido está na lista de allowed_roles
                if group in allowed_roles:
                    #se sim retorna a nossa view
                    return view(request, *args, **kwargs)
                else:
                    #Caso contrário exibe uma mensage que é proibido acessar usando HttpResponse
                    return HttpResponse('You are not authorized to acess this!!')

        #retorna para decorator o resultado de wrapper_func
        return wrapper_func
    #Retorna o decorator para a função que chamou
    return decorator



#Somente admin irá ter acesso à essa view
def admin_only(view):

    #Função que irá receber a view
    def wrapper_func(request, *args, **kwargs):
        #Inicialização da var group
        group = None

        #Verifica-se se o usuário possui algum group
        if request.user.groups.exists():
            #Caso sim, pega todos e retorna o nome do primeiro
            group = request.user.groups.all()[0].name

            #Caso esse group se chame customer redireciona para user_page
            if group == 'customer':
                return redirect('user_page')
            else:
                #Caso contrátrio segue a view
                return view(request, *args, *kwargs)

    #Retorna o resultado para o decorator
    return wrapper_func
