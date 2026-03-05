from django.contrib import admin
from .models import PesquisaClima, Pergunta, RespostaClima, RespostaPergunta

# 1. Configuração para criar perguntas dentro da Pesquisa
class PerguntaInline(admin.TabularInline):
    model = Pergunta
    extra = 1
    fields = ('texto', 'tipo', 'obrigatoria')

@admin.register(PesquisaClima)
class PesquisaClimaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativa', 'data_inicio')
    list_filter = ('ativa',)
    inlines = [PerguntaInline]

# 2. Configuração para ver as respostas dinâmicas dentro da Resposta Geral
class RespostaPerguntaInline(admin.TabularInline):
    model = RespostaPergunta
    extra = 0
    # Impede que o admin edite as respostas dos funcionários por aqui
    readonly_fields = ('pergunta', 'resposta_texto', 'resposta_nota')
    can_delete = False

@admin.register(RespostaClima)
class RespostaClimaAdmin(admin.ModelAdmin):
    # CORREÇÃO AQUI: nota_satisfacao mudou para nota_enps
    list_display = ('pesquisa', 'nota_enps', 'sentimento', 'setor', 'data_envio')
    list_filter = ('pesquisa', 'sentimento', 'setor')
    readonly_fields = ('data_envio',)
    inlines = [RespostaPerguntaInline]