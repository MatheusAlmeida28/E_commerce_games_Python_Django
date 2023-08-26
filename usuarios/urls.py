from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('valida_cadastro/', views.valida_cadastro, name='valida_cadastro'),
    path('valida_login/', views.valida_login, name='valida_login'),
    path('send_confirmation_email/', views.send_confirmation_email, name='send_confirmation_email'),
    path('confirmar_conta/<str:token>', views.confirmar_conta, name='confirmar_conta'),
    path('sair/', views.sair, name='sair'),
]