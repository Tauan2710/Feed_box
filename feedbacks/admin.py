from django.contrib import admin
from .models import Feedback, Resposta, Comunicado

admin.site.register(Feedback)
admin.site.register(Resposta)

@admin.register(Comunicado)
class ComunicadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_criacao', 'ativo')
    search_fields = ('titulo', 'conteudo')

    # Restringe todas as ações apenas para superusuários
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser