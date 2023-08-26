from django.db import models
from usuarios.models import Usuario

class Games(models.Model):
    foto = models.FileField(null=True, blank=True)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    game_score = models.IntegerField()
    game_ativo = models.BooleanField()

    def __str__(self):
        return self.nome

class Carrinho(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    item = models.ManyToManyField(Games, through='ItemCarrinho')
    data_atual = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario.username

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    games = models.ForeignKey(Games, on_delete=models.CASCADE)

    def __str__(self):
        return self.carrinho.usuario.username

class Pedido(models.Model):
    usuario = models.ManyToManyField(Usuario)
    games = models.ManyToManyField(Games)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_pedido = models.DateTimeField(auto_now_add=True)
    endereco_entrega = models.CharField(max_length=200)
    

