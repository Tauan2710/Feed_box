"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          FEEDBOX — EXPLICAÇÃO TÉCNICA DAS TECNOLOGIAS UTILIZADAS           ║
║          Análise de Sentimentos · Métrica NPS/eNPS · Motor de IA           ║
╚══════════════════════════════════════════════════════════════════════════════╝

  Projeto : Feedbox — Sistema de Feedback Corporativo
  Autor   : Talles
  Data    : 2026
  Arquivo : explicacao_tecnologias.py
  Propósito: Documentar e demonstrar as bibliotecas e algoritmos usados
             para análise de sentimentos, cálculo de NPS e o motor de IA
             implementado no projeto.

"""

# ==============================================================================
# SEÇÃO 1 — ANÁLISE DE SENTIMENTOS: Biblioteca TextBlob
# ==============================================================================
"""
📚 BIBLIOTECA USADA: TextBlob
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Site oficial : https://textblob.readthedocs.io/
  Instalação   : pip install textblob
  Consta em    : requirements.txt (linha 5)

  O QUE É?
  ─────────
  TextBlob é uma biblioteca Python para processamento de linguagem natural
  (NLP — Natural Language Processing). Ela fornece uma API simples e intuitiva
  para analisar texto e extrair informações como:
    → Polaridade emocional (positivo / negativo / neutro)
    → Subjetividade (o quanto o texto é opinativo)
    → Extração de frases-chave
    → Tradução de texto

  COMO USAMOS NO FEEDBOX?
  ───────────────────────
  Quando um funcionário envia um feedback, o sistema chama a função
  `analisar_sentimento_ia()` (em feedbacks/utils.py e feedbacks/views.py).
  Essa função usa o TextBlob para ler o texto e calcular a "polaridade":

    • polaridade > 0.1  →  Sentimento POSITIVO  😊
    • polaridade < -0.1 →  Sentimento NEGATIVO  😟
    • entre -0.1 e 0.1  →  Sentimento NEUTRO    😐

  O resultado é salvo no campo `sentimento` do model Feedback (banco de dados).

  EXEMPLO PRÁTICO (como funciona por baixo dos panos):
"""

try:
    from textblob import TextBlob

    print("=" * 60)
    print("  DEMONSTRAÇÃO — TextBlob (Análise de Sentimentos)")
    print("=" * 60)

    exemplos = [
        "Excellent work! I am very happy with the service.",   # Positivo (inglês)
        "The product is terrible and the service is slow.",   # Negativo (inglês)
        "The product arrived today.",                          # Neutro (inglês)
    ]

    for texto in exemplos:
        blob = TextBlob(texto)
        polaridade = blob.sentiment.polarity
        subjetividade = blob.sentiment.subjectivity

        if polaridade > 0.1:
            sentimento = "✅ POSITIVO"
        elif polaridade < -0.1:
            sentimento = "❌ NEGATIVO"
        else:
            sentimento = "⚪ NEUTRO"

        print(f"\n  Texto      : {texto}")
        print(f"  Polaridade : {polaridade:.3f}   (escala de -1.0 a +1.0)")
        print(f"  Subjetivo  : {subjetividade:.3f} (escala de 0 a 1)")
        print(f"  Resultado  : {sentimento}")

except ImportError:
    print("[AVISO] TextBlob não instalado. Execute: pip install textblob")


# ==============================================================================
# SEÇÃO 2 — LIMITAÇÃO DO TEXTBLOB E SOLUÇÃO APLICADA NO PROJETO
# ==============================================================================
"""
⚠️  LIMITAÇÃO IMPORTANTE — TextBlob foi treinado em textos em INGLÊS.
    Para textos em Português, a polaridade pode ser 0 (zero) com frequência.

  SOLUÇÃO APLICADA NO FEEDBOX:
  ─────────────────────────────
  Implementamos um sistema HÍBRIDO em duas camadas:

  CAMADA 1 — TextBlob (análise automática via NLP)
    → Tenta detectar o sentimento pelo modelo estatístico.
    → Se funcionar (polaridade ≠ 0), usa esse resultado.

  CAMADA 2 — Léxico Personalizado em Português (fallback manual)
    → Se o TextBlob retornar polaridade zero (não reconheceu o PT-BR),
      o sistema verifica se o texto contém palavras de um dicionário
      construído à mão para o contexto corporativo brasileiro.

    PALAVRAS POSITIVAS cadastradas no léxico:
      'bom', 'boa', 'ótimo', 'excelente', 'parabéns', 'gosto', 'gostei',
      'feliz', 'obrigado', 'ajudou', 'eficiente', 'sucesso'

    PALAVRAS NEGATIVAS cadastradas no léxico:
      'ruim', 'péssimo', 'horrível', 'difícil', 'problema', 'erro',
      'falha', 'atraso', 'absurdo', 'errado', 'pior', 'calor', 'quebrado'

  Esse modelo híbrido garante resultados muito mais confiáveis para
  feedbacks escritos em Português do Brasil.
"""

print("\n" + "=" * 60)
print("  DEMONSTRAÇÃO — Motor Híbrido em Português (Feedbox)")
print("=" * 60)


def analisar_sentimento_ia(texto):
    """
    Réplica exata da função usada no projeto Feedbox.
    Arquivo de origem: feedbacks/utils.py  e  feedbacks/views.py
    """
    if not texto:
        return 'Neutro'

    texto_lower = texto.lower()

    # --- CAMADA 1: TextBlob ---
    try:
        from textblob import TextBlob
        analise = TextBlob(texto)
        polaridade = analise.sentiment.polarity
        if polaridade > 0.1:
            return 'Positivo'
        elif polaridade < -0.1:
            return 'Negativo'
    except Exception:
        pass

    # --- CAMADA 2: Léxico PT-BR personalizado ---
    palavras_positivas = [
        'bom', 'boa', 'ótimo', 'otimo', 'excelente', 'parabéns',
        'parabens', 'gosto', 'gostei', 'feliz', 'obrigado',
        'ajudou', 'eficiente', 'sucesso'
    ]
    palavras_negativas = [
        'ruim', 'péssimo', 'pessimo', 'horrível', 'horrivel',
        'difícil', 'dificil', 'problema', 'erro', 'falha',
        'atraso', 'absurdo', 'errado', 'pior', 'calor', 'quebrado'
    ]

    if any(palavra in texto_lower for palavra in palavras_negativas):
        return 'Negativo'
    if any(palavra in texto_lower for palavra in palavras_positivas):
        return 'Positivo'

    return 'Neutro'


# Testando com frases em Português
feedbacks_exemplo = [
    "O atendimento foi excelente, parabéns à equipe!",
    "O sistema está com problema e o suporte demorou muito.",
    "Recebi o comunicado hoje.",
    "Ótimo trabalho pessoal, muito obrigado!",
    "Péssimo, o ar condicionado está quebrado há semanas.",
]

for fb in feedbacks_exemplo:
    resultado = analisar_sentimento_ia(fb)
    emoji = "✅" if resultado == "Positivo" else "❌" if resultado == "Negativo" else "⚪"
    print(f"\n  Feedback  : \"{fb}\"")
    print(f"  Resultado : {emoji} {resultado}")


# ==============================================================================
# SEÇÃO 3 — MÉTRICA eNPS (Employee Net Promoter Score)
# ==============================================================================
"""
📊 MÉTRICA USADA: eNPS — Employee Net Promoter Score
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Criador: Fred Reichheld (Bain & Company, 2003)
  Adaptação: eNPS = versão para funcionários (Employee)

  NÃO É UMA BIBLIOTECA EXTERNA — é um cálculo matemático puro
  implementado com Python nativo + ORM do Django.

  COMO FUNCIONA?
  ──────────────
  Os funcionários respondem: "Em uma escala de 0 a 10, o quanto
  você recomendaria a empresa como um bom lugar para trabalhar?"

  Com base na nota, cada respondente é classificado em:

    ┌─────────────┬────────────┬──────────────────────────────────┐
    │  Categoria  │   Notas    │ Significado                      │
    ├─────────────┼────────────┼──────────────────────────────────┤
    │ 😍 Promotor │   9 ou 10  │ Fã da empresa, engajado          │
    │ 😐 Neutro   │   7 ou 8   │ Satisfeito, mas sem entusiasmo   │
    │ 😠 Detrator │  0 a 6     │ Insatisfeito, risco de evasão    │
    └─────────────┴────────────┴──────────────────────────────────┘

  FÓRMULA DO eNPS:
  ────────────────

    eNPS = ((Nº Promotores - Nº Detratores) / Total de Respostas) × 100

  ESCALA DE INTERPRETAÇÃO:
  ────────────────────────
    •  -100 a -1  → Zona Crítica   ⚠️  (muitos detratores)
    •    0  a 49  → Zona de Alerta ⚡ (precisa melhorar)
    •   50  a 74  → Zona de Qualidade ✅
    •   75  a 100 → Zona de Excelência 🏆

  ONDE ESTÁ NO CÓDIGO?
  ────────────────────
  Arquivo: feedbacks/views.py  (função `dashboard`, linhas 104–119)
  Arquivo: clima/views.py      (função `ver_resultados_pesquisa`, linhas 98–104)
"""

print("\n" + "=" * 60)
print("  DEMONSTRAÇÃO — Cálculo eNPS (exatamente como no Feedbox)")
print("=" * 60)


def calcular_enps(notas: list) -> dict:
    """
    Réplica da lógica de cálculo eNPS usada no projeto Feedbox.
    No projeto real, 'notas' vem do banco de dados via Django ORM.
    """
    if not notas:
        return {"enps_score": 0, "promotores": 0, "neutros": 0, "detratores": 0, "total": 0}

    total = len(notas)
    promotores = sum(1 for n in notas if n >= 9)
    detratores = sum(1 for n in notas if n <= 6)
    neutros = sum(1 for n in notas if 7 <= n <= 8)

    enps_score = ((promotores - detratores) / total) * 100

    return {
        "enps_score": round(enps_score, 1),
        "promotores": promotores,
        "neutros": neutros,
        "detratores": detratores,
        "total": total,
    }


# Simulação de respostas de funcionários
notas_simuladas = [10, 9, 8, 10, 6, 3, 9, 7, 10, 5, 9, 8, 10, 4, 9]

resultado_enps = calcular_enps(notas_simuladas)

print(f"\n  Notas recebidas : {notas_simuladas}")
print(f"\n  Promotores  (9-10) : {resultado_enps['promotores']} funcionários")
print(f"  Neutros     (7-8)  : {resultado_enps['neutros']} funcionários")
print(f"  Detratores  (0-6)  : {resultado_enps['detratores']} funcionários")
print(f"  Total de respostas : {resultado_enps['total']}")
print(f"\n  Fórmula: (({resultado_enps['promotores']} - {resultado_enps['detratores']}) / {resultado_enps['total']}) × 100")
print(f"  ╔══════════════════════════════╗")
print(f"  ║  eNPS Score = {resultado_enps['enps_score']:>6.1f}          ║")
print(f"  ╚══════════════════════════════╝")

score = resultado_enps["enps_score"]
if score < 0:
    zona = "⚠️  Zona CRÍTICA — Prioridade máxima de ação!"
elif score < 50:
    zona = "⚡ Zona de ALERTA — Melhorias necessárias."
elif score < 75:
    zona = "✅ Zona de QUALIDADE — Bom resultado."
else:
    zona = "🏆 Zona de EXCELÊNCIA — Referência de mercado!"

print(f"  Interpretação: {zona}")


# ==============================================================================
# SEÇÃO 4 — O MOTOR DE "IA" DO PROJETO: O QUE É E O QUE NÃO É
# ==============================================================================
"""
🤖 O "MOTOR DE IA" DO FEEDBOX — ENTENDENDO A ARQUITETURA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  O projeto usa o termo "IA" para descrever o motor de análise automática
  de sentimentos. Veja o que está por baixo:

  CAMADA 1 — TextBlob (Modelo de Machine Learning)
  ─────────────────────────────────────────────────
  TextBlob usa internamente o NLTK (Natural Language Toolkit) e modelos
  treinados com Naive Bayes em corpus de textos rotulados. Isso é,
  tecnicamente, Machine Learning — portanto, sim, é uma forma de IA.
    → Tipo : Aprendizado Supervisionado (classificação de texto)
    → Modelo: Naive Bayes Classifier (treinado em inglês)
    → Saída : score de polaridade entre -1.0 e +1.0

  CAMADA 2 — Léxico PT-BR (Regras Heurísticas — "IA Simbólica")
  ──────────────────────────────────────────────────────────────
  O dicionário de palavras positivas/negativas em português é uma
  abordagem de IA Simbólica (baseada em regras), também chamada de
  "expert system" (sistema especialista). É mais antiga mas altamente
  eficaz para domínios específicos como o RH corporativo.

  ONDE O RESULTADO É SALVO?
  ─────────────────────────
  Modelo Feedback (banco de dados):
    campo `sentimento` → CharField com choices: 'Positivo', 'Neutro', 'Negativo'

  Modelo RespostaClima:
    campo `sentimento` → mesmo padrão, aplicado às pesquisas de clima

  FLUXO COMPLETO (do envio ao dashboard):
  ────────────────────────────────────────
  [Funcionário digita feedback]
        ↓
  [analisar_sentimento_ia(mensagem)]  ← AQUI entra o motor de IA
        ↓
  [TextBlob calcula polaridade]
        ↓  (se polaridade == 0)
  [Léxico PT-BR verifica palavras-chave]
        ↓
  [Sentimento salvo no banco: Positivo / Negativo / Neutro]
        ↓
  [Dashboard exibe gráfico de pizza com distribuição de sentimentos]

"""

print("\n" + "=" * 60)
print("  RESUMO EXECUTIVO — Stack Tecnológico do Feedbox")
print("=" * 60)
print("""
  ┌──────────────────┬──────────────────────────────────────────┐
  │  Funcionalidade  │  Tecnologia                              │
  ├──────────────────┼──────────────────────────────────────────┤
  │  Framework Web   │  Django 4.2 (Python)                    │
  │  Banco de Dados  │  SQLite (dev) via Django ORM             │
  │  Admin Interface │  django-jazzmin                          │
  │  API REST        │  Django REST Framework                   │
  │  Análise NLP     │  TextBlob (Naive Bayes + NLTK)          │
  │  Fallback PT-BR  │  Léxico customizado (heurística)         │
  │  Métrica eNPS    │  Cálculo matemático puro (Python)        │
  │  Motor de IA     │  TextBlob + Léxico Híbrido               │
  │  Servidor Prod.  │  Gunicorn + PythonAnywhere               │
  └──────────────────┴──────────────────────────────────────────┘
""")

print("  📁 Arquivos principais do motor de IA:")
print("     → feedbacks/utils.py     (função analisar_sentimento_ia)")
print("     → feedbacks/views.py     (aplicação no envio de feedbacks)")
print("     → clima/views.py         (aplicação nas pesquisas de clima)")
print("     → feedbacks/models.py    (campo `sentimento` no banco)")
print("     → requirements.txt       (dependência: textblob)")
print()
print("  ✅ Script executado com sucesso!")
print("=" * 60)
