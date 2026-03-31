import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback, Resposta, Comunicado
from .forms import RespostaForm
from setores.models import Setor
from django.db.models import Count, Avg
from clima.models import PesquisaClima, RespostaClima, Pergunta 
from textblob import TextBlob
from django.core.paginator import Paginator

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
    
    # Léxico de apoio técnico para o projeto Feedbox
    palavras_positivas = ['bom', 'boa', 'ótimo', 'otimo', 'excelente', 'parabéns', 'parabens', 'gosto', 'gostei', 'feliz', 'obrigado', 'ajudou', 'eficiente', 'sucesso']
    palavras_negativas = ['ruim', 'péssimo', 'pessimo', 'horrível', 'horrivel', 'difícil', 'dificil', 'problema', 'erro', 'falha', 'atraso', 'absurdo', 'errado', 'pior', 'calor', 'quebrado']
    
    if any(palavra in texto_lower for palavra in palavras_negativas):
        return 'Negativo'
    if any(palavra in texto_lower for palavra in palavras_positivas):
        return 'Positivo'
    return 'Neutro'

@login_required
def dashboard(request):
    user = request.user
    setor_id = request.GET.get('setor') 

    # Definição da base de dados de acordo com a permissão
    if user.is_superuser:
        feedbacks_base = Feedback.objects.all()
        setores_list = Setor.objects.all()
        pesquisas_recentes = PesquisaClima.objects.all().annotate(
            total_respostas=Count('respostas'),
            media_notas=Avg('respostas__nota_enps')
        ).order_by('-id')[:5]
        
        clima_dados_raw = RespostaClima.objects.values('nota_enps').annotate(total=Count('id')).order_by('nota_enps')
        clima_labels = [str(d['nota_enps']) for d in clima_dados_raw]
        clima_valores = [d['total'] for d in clima_dados_raw]
    else:
        feedbacks_base = Feedback.objects.filter(setor__responsavel=user)
        setores_list = Setor.objects.filter(responsavel=user)
        pesquisas_recentes = None
        clima_labels = []
        clima_valores = []

    # Aplicação de filtro por setor, se selecionado
    if setor_id:
        feedbacks_base = feedbacks_base.filter(setor_id=setor_id)

    # --- LÓGICA DE PAGINAÇÃO ---
    feedbacks_ordenados = feedbacks_base.select_related('setor').order_by('-data_criacao')
    paginator = Paginator(feedbacks_ordenados, 5) # 5 feedbacks por página
    page_number = request.GET.get('page')
    feedbacks_paginados = paginator.get_page(page_number)
    
    # KPIs Básicos (Calculados sobre a base total filtrada, não apenas a página)
    total = feedbacks_base.count()
    respondidos = feedbacks_base.filter(resposta__isnull=False).distinct().count()
    pendentes = total - respondidos
    
    # Gráfico de Sentimentos (IA)
    sentimentos_qs = feedbacks_base.values('sentimento').annotate(total=Count('id'))
    mapa_sentimentos = {'Positivo': 0, 'Neutro': 0, 'Negativo': 0}
    for item in sentimentos_qs:
        if item['sentimento'] in mapa_sentimentos:
            mapa_sentimentos[item['sentimento']] = item['total']
    
    sentimento_labels = ['Positivo', 'Neutro', 'Negativo']
    sentimento_valores = [mapa_sentimentos['Positivo'], mapa_sentimentos['Neutro'], mapa_sentimentos['Negativo']]

    # Gráfico de Categorias
    categorias_stats = feedbacks_base.values('categoria').annotate(total=Count('id'))
    mapa_nomes = {'SUGE': 'Sugestão', 'ELOG': 'Elogio', 'CRIT': 'Crítica', 'DENU': 'Denúncia'}
    categoria_labels = [mapa_nomes.get(c['categoria'], c['categoria']) for c in categorias_stats]
    categoria_valores = [c['total'] for c in categorias_stats]
    
    # Cálculo eNPS
    enps_score = 0
    total_enps = 0
    detratores_count = 0
    neutros_count = 0
    promotores_count = 0
    try:
        fbs_enps = feedbacks_base.exclude(nota_enps__isnull=True)
        total_enps = fbs_enps.count()
        if total_enps > 0:
            promotores_count = fbs_enps.filter(nota_enps__gte=9).count()
            detratores_count = fbs_enps.filter(nota_enps__lte=6).count()
            neutros_count = fbs_enps.filter(nota_enps__gte=7, nota_enps__lte=8).count()
            enps_score = ((promotores_count - detratores_count) / total_enps) * 100
    except Exception:
        enps_score = 0

    context = {
        'feedbacks': feedbacks_paginados,
        'total': total,
        'respondidos': respondidos,
        'pendentes': pendentes,
        'setores': setores_list,
        'pesquisas_recentes': pesquisas_recentes,
        'clima_labels': clima_labels,
        'clima_valores': clima_valores,
        'sentimento_labels': sentimento_labels,
        'sentimento_valores': sentimento_valores,
        'categoria_labels': categoria_labels,
        'categoria_valores': categoria_valores,
        'enps_score': round(enps_score, 1),
        'total_enps': total_enps,
        'detratores_count': detratores_count,
        'neutros_count': neutros_count,
        'promotores_count': promotores_count,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'feedbacks/_dashboard_feedback_section.html', context)
    return render(request, 'feedbacks/dashboard.html', context)

def enviar_feedback(request):
    protocolo_gerado = None
    if request.method == "POST":
        setor_id = request.POST.get('setor')
        mensagem = request.POST.get('mensagem')
        categoria = request.POST.get('categoria', 'SUGE')
        nota_enps = request.POST.get('nota_enps')
        eh_sensivel = request.POST.get('is_sensivel') == 'on'
        protocolo = None
        
        if eh_sensivel:
            protocolo = f"FB-{uuid.uuid4().hex[:4].upper()}"
            protocolo_gerado = protocolo
            categoria = 'DENU'
            
        if setor_id and mensagem:
            setor_obj = get_object_or_404(Setor, id=setor_id)
            Feedback.objects.create(
                setor=setor_obj,
                mensagem=mensagem,
                categoria=categoria,
                nota_enps=int(nota_enps) if nota_enps and nota_enps.isdigit() else None,
                sentimento=analisar_sentimento_ia(mensagem),
                is_sensivel=eh_sensivel,
                protocolo=protocolo
            )
            
            if eh_sensivel:
                setores = Setor.objects.all()
                feedbacks_lista = Feedback.objects.filter(is_sensivel=False).order_by('-data_criacao')
                paginator = Paginator(feedbacks_lista, 5)
                feedbacks_paginados = paginator.get_page(1)
                return render(request, 'feedbacks/enviar_feedback.html', {
                    'setores': setores,
                    'feedbacks': feedbacks_paginados,
                    'protocolo_sucesso': protocolo_gerado,
                })
            return redirect('enviar_feedback')
    
    setores = Setor.objects.all()
    feedbacks_lista = Feedback.objects.filter(is_sensivel=False).order_by('-data_criacao')
    paginator = Paginator(feedbacks_lista, 5)
    page_number = request.GET.get('page')
    feedbacks_paginados = paginator.get_page(page_number)
    context = {
        'setores': setores,
        'feedbacks': feedbacks_paginados,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'feedbacks/_mural_transparencia.html', context)
    return render(request, 'feedbacks/enviar_feedback.html', context)

@login_required
def responder_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.feedback = feedback
            resposta.save()
            feedback.lido = True
            feedback.save()
            messages.success(request, "Resposta enviada com sucesso!")
            return redirect('dashboard')
    else:
        form = RespostaForm()
    return render(request, 'feedbacks/responder_feedback.html', {'feedback': feedback, 'form': form})

def curtir_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id, is_sensivel=False)
    feedback.curtidas += 1
    feedback.save()
    return redirect(request.META.get('HTTP_REFERER', 'enviar_feedback'))

def consultar_protocolo(request):
    feedback = None
    protocolo = request.GET.get('protocolo')
    erro = None
    if protocolo:
        feedback = Feedback.objects.filter(protocolo=protocolo.strip().upper()).first()
        if not feedback:
            erro = "Protocolo não encontrado."
    return render(request, 'feedbacks/consultar_protocolo.html', {'feedback': feedback, 'erro': erro, 'protocolo': protocolo})

def listar_comunicados(request):
    comunicados = Comunicado.objects.filter(ativo=True).order_by('-data_criacao')
    return render(request, 'feedbacks/listar_comunicados.html', {'comunicados': comunicados})

@login_required
def gerenciar_mural(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    comunicados = Comunicado.objects.all().order_by('-data_criacao')
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        if titulo and conteudo:
            Comunicado.objects.create(titulo=titulo, conteudo=conteudo, ativo=True)
            messages.success(request, "Comunicado postado com sucesso!")
            return redirect('gerenciar_mural')
    return render(request, 'feedbacks/gerenciar_mural.html', {'comunicados': comunicados})

@login_required
def editar_comunicado(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboard')
    comunicado = get_object_or_404(Comunicado, pk=pk)
    if request.method == "POST":
        comunicado.titulo = request.POST.get('titulo')
        comunicado.conteudo = request.POST.get('conteudo')
        comunicado.ativo = 'ativo' in request.POST
        comunicado.save()
        messages.success(request, "Comunicado atualizado!")
        return redirect('gerenciar_mural')
    return render(request, 'feedbacks/editar_comunicado.html', {'comunicado': comunicado})

@login_required
def excluir_comunicado(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboard')
    comunicado = get_object_or_404(Comunicado, pk=pk)
    comunicado.delete()
    messages.error(request, "Comunicado excluído com sucesso.")
    return redirect('gerenciar_mural')

@login_required
def nova_pesquisa_clima(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        perguntas_texto = request.POST.getlist('pergunta_texto[]')
        perguntas_tipo = request.POST.getlist('pergunta_tipo[]')
        if titulo:
            pesquisa = PesquisaClima.objects.create(titulo=titulo, ativa=True)
            for texto, tipo in zip(perguntas_texto, perguntas_tipo):
                if texto.strip():
                    Pergunta.objects.create(pesquisa=pesquisa, texto=texto, tipo=tipo.upper())
            messages.success(request, f"Pesquisa '{titulo}' lançada com sucesso!")
            return redirect('dashboard')
    return render(request, 'feedbacks/nova_pesquisa_clima.html')