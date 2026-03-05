
from django import forms
from .models import Feedback, Resposta
from setores.models import Setor

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['setor', 'mensagem']
        widgets = {
            'mensagem': forms.Textarea(attrs={'placeholder': 'Escreva seu feedback anônimo aqui...', 'rows': 4}),
        }

class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['texto_resposta']