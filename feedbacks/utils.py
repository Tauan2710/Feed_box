# pyrefly: ignore [missing-import]
from textblob import TextBlob

def analisar_sentimento_ia(texto):
    """
    Motor de IA para análise de sentimentos.
    Utiliza TextBlob para polaridade e um léxico de suporte para Português.
    """
    if not texto:
        return 'Neutro'
    texto_lower = texto.lower()
    try:
        analise = TextBlob(texto)
        polaridade = analise.sentiment.polarity
        if polaridade > 0.1:
            return 'Positivo'
        elif polaridade < -0.1:
            return 'Negativo'
    except:
        pass

    # (Léxico de apoio técnico para o projeto Feedbox) 
    # (aqui foi colocado para ajudar a IA a entender melhor o nosso contexto)
    palavras_positivas = ['bom', 'boa', 'ótimo', 'otimo', 'excelente', 'parabéns', 'parabens', 'gosto', 'gostei', 'feliz', 'obrigado', 'ajudou', 'eficiente', 'sucesso']
    palavras_negativas = ['ruim', 'péssimo', 'pessimo', 'horrível', 'horrivel', 'difícil', 'dificil', 'problema', 'erro', 'falha', 'atraso', 'absurdo', 'errado', 'pior', 'calor', 'quebrado']
    
    if any(palavra in texto_lower for palavra in palavras_negativas):
        return 'Negativo'
    if any(palavra in texto_lower for palavra in palavras_positivas):
        return 'Positivo'
    return 'Neutro'
