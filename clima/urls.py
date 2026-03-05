from django.urls import path
from . import views

urlpatterns = [
    # Rota que o botão do seu dashboard chama
    path('', views.listar_pesquisas, name='listar_pesquisas'),
    
    # Rota nova exclusiva para o Painel do Admin
    path('gerenciar/', views.gerenciar_pesquisas_admin, name='gerenciar_pesquisas'),
    
    path('responder/<int:pesquisa_id>/', views.responder_pesquisa, name='responder_pesquisa'),
    path('resultados/<int:pesquisa_id>/', views.ver_resultados_pesquisa, name='resultados_pesquisa'),
    path('pesquisa/editar/<int:pesquisa_id>/', views.editar_pesquisa, name='editar_pesquisa'),
    path('pesquisa/excluir/<int:pesquisa_id>/', views.excluir_pesquisa, name='excluir_pesquisa'),
]