from django.shortcuts import render, redirect
from .models import Games, Carrinho, ItemCarrinho, Pedido
from usuarios.models import Usuario

def adicionar_ao_carrinho(request, game_id):
    if not request.user.is_authenticated:
        return redirect('/acesso/login/')
    
    game = Games.objects.get(id=game_id)
    carrinho = Carrinho.objects.get(usuario_id=request.user)

    item, created = ItemCarrinho.objects.get_or_create(
        carrinho_id=carrinho.id,
        games_id=game.id)

    item.save()
    return redirect('/plataforma/home/')

def remover_do_carrinho(request, item_id):
    if not request.user.is_authenticated:
        return redirect('/acesso/login/')
    
    game = Games.objects.get(id=item_id)
    carrinho = Carrinho.objects.get(usuario_id=request.user)

    item, created = ItemCarrinho.objects.get_or_create(
        carrinho_id=carrinho.id,
        games_id=game.id)

    item.delete()
    
    return redirect('/plataforma/home/')

def remover_item_carrinho_checkout(request, item_id):
    if not request.user.is_authenticated:
        return redirect('/acesso/login/')
    
    game = Games.objects.get(id=item_id)
    carrinho = Carrinho.objects.get(usuario_id=request.user)

    item, created = ItemCarrinho.objects.get_or_create(
        carrinho_id=carrinho.id,
        games_id=game.id)

    item.delete()
    
    return redirect('/plataforma/checkout/')

def _calcular_preco_final(itens):
    preco_final = 0
    frete = 0
    soma = 0
    for item in itens:
        soma += item.games.preco
        frete += 10
    if soma >= 250:
        frete = 0
        preco_final = soma
    else:
        preco_final = frete + soma
    return preco_final, frete, soma


def home(request):
    if not request.user.is_authenticated:
        return redirect('/acesso/login/')  
    
    carrinho = Carrinho.objects.get(usuario=request.user)
    itens = ItemCarrinho.objects.filter(carrinho=carrinho)
    games = Games.objects.all()
       
    no_carrinho = []
    for item in itens:
        no_carrinho.append(1)
    
    preco_final, frete, soma = _calcular_preco_final(itens)
    
    order_by = request.GET.get('order_by')
    if order_by == 'preco':
        games = Games.objects.all().order_by('preco')
    elif order_by == 'popularidade':
        games = Games.objects.all().order_by('-game_score')
    elif order_by == 'alfabetica':
        games = Games.objects.all().order_by('nome')
    else:
        games = Games.objects.all()

    return render(request, 'home.html', {'games_carrinho': itens,
                                          'soma': soma,
                                          'frete':frete,
                                          'preco_final':preco_final,
                                          'no_carrinho': no_carrinho,
                                          'games': games})

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('/acesso/login/')
    
    carrinho = Carrinho.objects.get(usuario_id=request.user)
    itens = ItemCarrinho.objects.filter(carrinho=carrinho)

    no_carrinho = []
    for item in itens:
        no_carrinho.append(1)
    
    preco_final, frete, soma = _calcular_preco_final(itens)


    return render(request, 'checkout.html', {'games_carrinho': itens,
                                            'soma': soma,
                                            'frete':frete,
                                            'preco_final':preco_final,
                                            'no_carrinho': no_carrinho,})

def processar_checkout(request):  
    if not request.user.is_authenticated:
        return redirect('/acesso/login/')
    
    if request.method == "POST":
        usuario = Usuario.objects.get(id=request.user.id)
        carrinho = Carrinho.objects.get(usuario_id=request.user)
        itens = ItemCarrinho.objects.filter(carrinho=carrinho)

        preco_final, frete, soma = _calcular_preco_final(itens)

        pedido, created = Pedido.objects.get_or_create(preco=preco_final,
                                                    endereco_entrega=usuario.endereco)

        pedido.usuario.add(usuario)
        
        for item in itens:
            pedido.games.add(item.games)

        pedido.save()
        
        itens.delete()
        carrinho.delete()

        carrinho_novo = Carrinho.objects.create(usuario_id=request.user.id)
        carrinho_novo.save()

        return redirect('/plataforma/endereco_e_pedidos')


def endereco_e_pedidos(request):
    if not request.user.is_authenticated:
        return redirect('/acesso/login/')
    
    pedidos = Pedido.objects.filter(usuario=request.user)
    estados_br = Usuario.estados_br

    return render(request, 'endereco_e_pedidos.html', {'pedidos': pedidos, 'estados_br': estados_br})
