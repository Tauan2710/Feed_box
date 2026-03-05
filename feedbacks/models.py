from django.db import models
from setores.models import Setor

class Feedback(models.Model):
    CATEGORIA_CHOICES = [
        ('SUGE', 'Sugestão'),
        ('ELOG', 'Elogio'),
        ('RECL', 'Reclamação'),
        ('ENPS', 'eNPS'),
        ('DENU', 'Denúncia'), # Adicionada categoria denúncia
    ]

    SENTIMENTO_CHOICES = [
        ('Positivo', 'Positivo'),
        ('Negativo', 'Negativo'),
        ('Neutro', 'Neutro'),
    ]

    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='feedbacks')
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)
    curtidas = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=4, choices=CATEGORIA_CHOICES, default='SUGE')
    nota_enps = models.PositiveIntegerField(null=True, blank=True)
    sentimento = models.CharField(max_length=20, choices=SENTIMENTO_CHOICES, null=True, blank=True, default='Neutro')

    # --- NOVOS CAMPOS ---
    is_sensivel = models.BooleanField(default=False)
    protocolo = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Feedback {self.id} - {self.setor.nome}"

class Resposta(models.Model):
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE, related_name='resposta')
    texto_resposta = models.TextField()
    data_resposta = models.DateTimeField(auto_now_add=True)
    
    from django.db import models

class Comunicado(models.Model):
    TIPOS = (
        ('AVIS', 'Aviso'),
        ('IMPO', 'Importante'),
        ('DEST', 'Destaque'),
    )
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=4, choices=TIPOS, default='AVIS')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo