from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Feedback, Resposta
from setores.models import Setor

@login_required
def dashboard(request):
    feedbacks = Feedback.objects.select_related('setor').order_by('-id')

    total = feedbacks.count()
    respondidos = feedbacks.filter(respondido=True).count()
    pendentes = feedbacks.filter(respondido=False).count()

    # Gráfico por setor
    setores = (
        feedbacks
        .values('setor__nome')
        .annotate(total=Count('id'))
        .order_by('setor__nome')
    )

    setores_labels = [s['setor__nome'] for s in setores]
    setores_data = [s['total'] for s in setores]

    context = {
        'feedbacks': feedbacks,
        'total': total,
        'respondidos': respondidos,
        'pendentes': pendentes,
        'setores_labels': setores_labels,
        'setores_data': setores_data,
    }

    return render(request, 'dashboard.html', context)


@login_required
def responder_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == 'POST':
        texto = request.POST.get('resposta')

        Resposta.objects.create(
            feedback=feedback,
            texto=texto,
            autor=request.user
        )

        feedback.respondido = True
        feedback.save()

        return redirect('dashboard')

    return render(request, 'responder_feedback.html', {'feedback': feedback})
def dashboard(request):
    user = request.user
    setor_id = request.GET.get('setor') # Captura o filtro da URL
    
    # 1. Filtro de Permissão (Quem pode ver o quê)
    if user.is_superuser:
        feedbacks_base = Feedback.objects.all()
    else:
        # Filtra feedbacks onde o responsável pelo setor é o usuário logado
        feedbacks_base = Feedback.objects.filter(setor__responsavel=user)

    # 2. Filtro de Busca (Barra de pesquisa por setor)
    if setor_id:
        feedbacks_base = feedbacks_base.filter(setor_id=setor_id)

    feedbacks = feedbacks_base.order_by('-data_criacao')
    
    # Métricas baseadas no que o usuário tem permissão de ver
    total = feedbacks.count()
    respondidos = feedbacks.filter(resposta__isnull=False).distinct().count()
    pendentes = total - respondidos
    
    # Para preencher o <select> de busca no HTML
    setores = Setor.objects.all() if user.is_superuser else Setor.objects.filter(responsavel=user)

    context = {
        'feedbacks': feedbacks,
        'total': total,
        'respondidos': respondidos,
        'pendentes': pendentes,
        'setores': setores,
    }
    return render(request, 'feedbacks/dashboard.html', context)