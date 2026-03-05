from django.contrib import admin
from .models import Setor

# Use APENAS o decorador OU o admin.site.register, nunca os dois.
@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'responsavel')
    search_fields = ('nome',)

# Certifique-se de que NÃO EXISTE uma linha como: admin.site.register(Setor) aqui embaixo.