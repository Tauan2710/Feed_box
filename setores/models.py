from django.db import models

class Setor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    
    # Este campo permite vincular um administrador ao setor
    responsavel = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='setores_gerenciados'
    )

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.nome