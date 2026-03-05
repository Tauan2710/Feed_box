from django import forms
from .models import PesquisaClima

class PesquisaClimaForm(forms.ModelForm):
    class Meta:
        model = PesquisaClima
        fields = ['titulo', 'setor', 'ativa']
from .models import Pergunta


class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = ['texto']
