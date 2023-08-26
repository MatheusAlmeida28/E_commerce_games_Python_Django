from django.urls import path
from .  import views  

urlpatterns = [
    path('adicionar/<int:game_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover/<int:item_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('home/', views.home, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('remover_item_carrinho_checkout/<int:item_id>', views.remover_item_carrinho_checkout, name='remover_item_carrinho_checkout'),
    path('processar_checkout/', views.processar_checkout, name='processar_checkout'),   
    path('endereco_e_pedidos/', views.endereco_e_pedidos, name='endereco_e_pedidos')
]
