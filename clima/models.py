from django.db import models
from setores.models import Setor

class PesquisaClima(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título da Pesquisa")
    descricao = models.TextField(blank=True, verbose_name="Descrição/Objetivo")
    ativa = models.BooleanField(default=True, verbose_name="Pesquisa Ativa?")
    data_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Pesquisa de Clima"
        verbose_name_plural = "Pesquisas de Clima"

class Pergunta(models.Model):
    TIPO_CHOICES = [
        ('NOTA', 'Escala de Emoji (1-5)'),
        ('TEXTO', 'Resposta Discursiva (Texto)'),
    ]

    pesquisa = models.ForeignKey(PesquisaClima, on_delete=models.CASCADE, related_name='perguntas')
    texto = models.CharField(max_length=255, verbose_name="Pergunta")
    tipo = models.CharField(
        max_length=10, 
        choices=TIPO_CHOICES, 
        default='NOTA',
        verbose_name="Tipo de Resposta"
    )
    obrigatoria = models.BooleanField(default=True, verbose_name="É obrigatória?")

    def __str__(self):
        return f"{self.texto} ({self.get_tipo_display()})"

class RespostaClima(models.Model):
    """
    Guarda o 'cabeçalho' da resposta: Quem respondeu (setor), 
    os dados fixos de eNPS e a análise de IA.
    """
    SENTIMENTO_CHOICES = [
        ('Positivo', 'Positivo'),
        ('Negativo', 'Negativo'),
        ('Neutro', 'Neutro'),
    ]

    pesquisa = models.ForeignKey(PesquisaClima, on_delete=models.CASCADE, related_name='respostas')
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campo Fixo: Régua 0-10 (eNPS)
    nota_enps = models.PositiveIntegerField(verbose_name="Nota eNPS (0-10)") 
    
    # Campo Fixo: Comentário para Análise de Sentimento (IA)
    comentario_ia = models.TextField(null=True, blank=True, verbose_name="Comentário para IA")
    sentimento = models.CharField(max_length=20, choices=SENTIMENTO_CHOICES, default='Neutro')
    
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"eNPS: {self.nota_enps} | Sentimento: {self.sentimento}"

class RespostaPergunta(models.Model):
    """
    Aqui é onde salvamos as respostas das perguntas DINÂMICAS 
    que você criou na PesquisaClima.
    """
    resposta_clima = models.ForeignKey(RespostaClima, on_delete=models.CASCADE, related_name='detalhes')
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    
    # Se a pergunta for TEXTO, preenchemos este:
    resposta_texto = models.TextField(null=True, blank=True)
    
    # Se a pergunta for NOTA (Emoji), preenchemos este (1-5):
    resposta_nota = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Resposta para: {self.pergunta.texto}"