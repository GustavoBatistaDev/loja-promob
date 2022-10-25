from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.messages import constants
import re
from django.db.models import Q
import hashlib
from .models import Token
from .utils import email_html
from valemoveis import settings
from pathlib import Path



def cadastro(request):

    if request.user.is_authenticated:
        return redirect('/') 

    if request.method == 'GET':
        return render(request, 'cadastro.html')


    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            repetir_senha = request.POST.get('repetir_senha')
           

            if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or\
                len(repetir_senha.strip()) == 0:

                messages.add_message(request, constants.ERROR, 'Nenhum campo pode ser mulo.')
                return redirect('cadastro')
            
            else:
                username = username.strip()
                email = email.strip()
                senha = senha.strip()
                repetir_senha = repetir_senha.strip()



                if senha != repetir_senha:
                    messages.add_message(request, constants.ERROR, 'Senhas não conferem.')
                    return redirect('cadastro')
                
                elif not re.search('[A-Z]', senha):
                    messages.add_message(request, constants.ERROR, 'Sua senha precisa ter letras maiúsculas.')
                    return redirect('cadastro')

                elif not re.search('[a-z]', senha):
                    messages.add_message(request, constants.ERROR, 'Sua senha precisa ter letras minúsculas' )
                    return redirect('cadastro')

                elif len(senha) < 8:
                    messages.add_message(request, constants.ERROR, 'Sua senha precisa ter no mínimo 8 caracteres.' )
                    return redirect('cadastro')

                query = Q(
                    Q(email=email)|Q(username=username)
                )
                userr = User.objects.filter(query)
                if len(userr) > 0:
                    messages.add_message(request, constants.ERROR, 'Usuário ou email já cadastrados. Faça login')
                    return redirect('login')

                try:
                    user = User.objects.create_user(
                                                    username=username,
                                                    password=senha,
                                                    email=email,
                                                    is_active=False,
                                                
                                                    
                                                    )

                    user.save()

                    
                except:
                    messages.add_message(request, constants.ERROR, 'Erro interno do sistema.Tente novamente em instantes.')
                    return redirect('cadastro')

                user_id = User.objects.get(id=user.id)

                token = hashlib.sha256(f'{username}{email}'.encode()).hexdigest()
                try:
                    token_usuario = Token(usuario_id=user_id.id, token=token)
                    token_usuario.save()


                except:
                    pass

                try:   
                    path_template = Path(settings.BASE_DIR, 'autenticacao/templates/email/email.html')
                    
                    email_html(path_template=path_template, assunto= 'Autentique a sua conta para fazer login no sistema Vale Móveis.', 
                                para=[email,], link_ativacao=f'http://127.0.0.1:8000/auth/ativacao/{token}', usuario=username )
                    messages.add_message(request, constants.SUCCESS, 'Você foi cadastrado. Agora Verifique seu email.')
                    return redirect('login')
                except:
                    messages.add_message(request, constants.ERROR, 'Erro interno do sistema. Tente novamente em instantes.')
                    return redirect('cadastro')



            

        

def ativacao(request, token):
    usuario_token = Token.objects.get(token=token)
    usuario_user = User.objects.get(id=usuario_token.usuario.id)

    if usuario_token.validade:
        messages.add_message(request, constants.WARNING, 'Essa conta já foi autenticada.')
        return redirect('cadastro')

    usuario_token.validade = True
    usuario_token.save()

    usuario_user.is_active = True
    usuario_user.save()
    messages.add_message(request, constants.SUCCESS, 'Sua conta está autenticada. Agora faça login.')
    return redirect('login')



 


def login(request):
    if request.user.is_authenticated:
        return redirect('/') 

    if request.method == 'GET':
        return render(request, 'login.html')


    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            senha = request.POST.get('senha')

            if len(username.strip()) == 0 or len(senha.strip()) == 0:
                messages.add_message(request, constants.ERROR, 'Nenhum campo pode ser nulo.')
                return redirect('login')

            usuario = auth.authenticate(username=username, password=senha)
            if usuario:
                auth.login(request, usuario)
                return redirect('home')

            else:
                messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos.')
                return redirect('login')



          
def sair(request):
    auth.logout(request)
    return redirect('login')

