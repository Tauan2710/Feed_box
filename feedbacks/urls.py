from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('enviar-feedback/', views.enviar_feedback, name='enviar_feedback'),
    path('responder/<int:feedback_id>/', views.responder_feedback, name='responder_feedback'),
    path('curtir/<int:feedback_id>/', views.curtir_feedback, name='curtir_feedback'),
    path('consultar-protocolo/', views.consultar_protocolo, name='consultar_protocolo'),
    path('comunicados/', views.listar_comunicados, name='listar_comunicados'),
    path('mural/gerenciar/', views.gerenciar_mural, name='gerenciar_mural'),
    path('mural/editar/<int:pk>/', views.editar_comunicado, name='editar_comunicado'),
    path('mural/excluir/<int:pk>/', views.excluir_comunicado, name='excluir_comunicado'),
    path('clima/nova-pesquisa/', views.nova_pesquisa_clima, name='nova_pesquisa_clima'),
]