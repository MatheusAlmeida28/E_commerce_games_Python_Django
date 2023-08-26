from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import messages, auth
from django.core.mail import send_mail
from plataforma.models import Carrinho


def login(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    
    return render(request, 'login_cadastro.html')

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    
    estados_br = Usuario.estados_br

    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status, 'estados_br': estados_br})


def send_confirmation_email(request):
    subject = 'Confirme sua conta'
    message = 'Clique no link para confirmar sua conta: http://127.0.0.1:8000/acesso/confirmar_conta/' + request.confirmation_token 
    from_email = 'gamessuperatecnologia@gmail.com'
    recipient_list = [request.email]
    send_mail(subject, message, from_email, recipient_list)


def confirmar_conta(request, token):  
    try:
        usuario = Usuario.objects.get(confirmation_token=token)
    except Usuario.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Usuário não existe.')
        return redirect('/acesso/login/')

    if usuario.is_active == True:
        messages.add_message(request, constants.INFO, 'Token expirado: Usuário já cadastrado')
        return redirect('/plataforma/home/')

    elif usuario:
        usuario.is_active = True    
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Conta confirmada com sucesso!')
        auth.login(request, usuario)
        return redirect('/plataforma/home/')
    else:
        messages.add_message(request, constants.ERROR, 'Token inválido.')
        return redirect('/acesso/login/')


def valida_cadastro(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    
    email = request.POST.get('email')
    confimaremail = request.POST.get('confirmaremail')
    senha = request.POST.get('senha')
    confirmarsenha = request.POST.get('confirmarsenha')
    nome_completo = request.POST.get('nome_completo')
    cpf = request.POST.get('cpf')
    telefone = request.POST.get('telefone')
    cep = request.POST.get('cep')
    numero_casa = request.POST.get('numero_casa')
    endereco = request.POST.get('endereco')
    cidade = request.POST.get('cidade')
    bairro = request.POST.get('bairro')
    estado = request.POST.getlist('estado')[0]


    cpf_validar = cpf.replace(".", "").replace("-", "")
    
    

    if len(nome_completo.strip()) == 0 or len(email.strip()) == 0 or len(confimaremail.strip()) == 0 or len(senha.strip()) == 0:
        messages.add_message(request, constants.ERROR,'Campos como Nome Completo, senha e email não podem estar vazios')
        return redirect('/acesso/cadastro/')
    
    elif len(endereco.strip()) == 0 or len(cidade.strip()) == 0 or len(bairro.strip()) == 0 or len(numero_casa.strip()) == 0:
        messages.add_message(request, constants.ERROR,'Campos como Endereço, Cidade, Bairro e Número da Casa não podem estar vazios')
        return redirect('/acesso/cadastro/')


    elif Usuario.objects.filter(email=email).exists():
        messages.add_message(request, constants.ERROR, 'Email já Cadastrado')
        return redirect('/acesso/cadastro/')

    elif email != confimaremail:
        messages.add_message(request, constants.ERROR, 'Emails não são iguais ')
        return redirect('/acesso/cadastro/')

    elif senha != confirmarsenha: 
        messages.add_message(request, constants.ERROR,
                             'As senhas não estão iguais')
        return redirect('/acesso/cadastro/')
    
    elif len(senha) < 8:
        messages.add_message(request, constants.ERROR,
                             'Sua senha deve ter no minino 8 digitos')
        return redirect('/acesso/cadastro/')
    
    elif len(cep.strip()) == 0:
        messages.add_message(request, constants.ERROR,
                             'O campo cep não pode estar vazio')
        return redirect('/acesso/cadastro/')

    elif len(telefone.strip()) == 0:
        messages.add_message(request, constants.ERROR,
                             'O campo telefone não pode estar vazio')
        return redirect('/acesso/cadastro/')

    elif len(cpf.strip()) == 0:
        messages.add_message(request, constants.ERROR,
                             'O campo cpf não pode estar vazio')
        return redirect('/acesso/cadastro/')
    
       
    usuario = Usuario.objects.create_user(
            username = email,
            nome_completo=nome_completo, 
            email=email, 
            password=senha,
            cpf=cpf_validar,
            telefone=telefone,
            cep=cep,
            numero_casa=numero_casa,
            endereco=endereco,
            cidade=cidade,
            bairro=bairro,
            estado=estado,
            is_active=False)
        
    usuario.save()

    carrinho_novo = Carrinho.objects.create(usuario_id=usuario.id)
    carrinho_novo.save()

    send_confirmation_email(usuario)
    messages.add_message(request, constants.SUCCESS,
                'Cadastro feito com Sucesso, Valide sua conta verificando no email ou spam do email')
    return redirect('/acesso/login/')


def valida_login(request):
    if request.user.is_authenticated:
        return redirect('/plataforma/home')
    
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    try:
        usuario = Usuario.objects.get(username=email)
    except Usuario.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Usuário não encontrado')
        return redirect('/acesso/login/')
    
    if not usuario.is_active:
        messages.add_message(request, constants.ERROR,
                             'Conta não confirmada, verifique seu email')
        return redirect('/acesso/login/')

    usuario = auth.authenticate(username=email, password=senha)

    if usuario is None:
        messages.add_message(request, constants.ERROR,
                             'Nome ou senha inválidos')
        return redirect('/acesso/login/')
       
    auth.login(request, usuario)
    return redirect('/plataforma/home/')


def sair(request):
    auth.logout(request)
    return redirect('/acesso/login/')

