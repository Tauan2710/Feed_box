from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PesquisaClima, Pergunta, RespostaClima, RespostaPergunta
from setores.models import Setor
from feedbacks.views import analisar_sentimento_ia 

@login_required
def listar_pesquisas(request):
    """
    Esta view atende o botão 'Responder' do Dashboard.
    Ela sempre mostrará a tela do usuário com pesquisas ATIVAS.
    """
    pesquisas = PesquisaClima.objects.filter(ativa=True).order_by('-data_inicio')
    return render(request, 'clima/listar_pesquisas_usuario.html', {'pesquisas': pesquisas})

@login_required
def gerenciar_pesquisas_admin(request):
    """
    Esta view é exclusiva para o Administrador gerenciar (Editar/Excluir).
    """
    if not request.user.is_superuser:
        return redirect('listar_pesquisas')
    
    pesquisas = PesquisaClima.objects.all().order_by('-data_inicio')
    return render(request, 'clima/gerenciar_pesquisas.html', {'pesquisas': pesquisas})

@login_required
def responder_pesquisa(request, pesquisa_id):
    pesquisa = get_object_or_404(PesquisaClima, id=pesquisa_id)
    
    if not pesquisa.ativa and not request.user.is_superuser:
        messages.error(request, "Esta pesquisa não está mais aceitando respostas.")
        return redirect('listar_pesquisas')

    setores = Setor.objects.all()
    perguntas = pesquisa.perguntas.all()

    if request.method == "POST":
        setor_id = request.POST.get('setor')
        nota_enps = request.POST.get('nota_enps')
        texto_do_form = request.POST.get('detalhes', '') 
        
        sentimento_detectado = analisar_sentimento_ia(texto_do_form)
        
        if nota_enps and setor_id:
            resposta_pai = RespostaClima.objects.create(
                pesquisa=pesquisa,
                setor_id=setor_id,
                nota_enps=int(nota_enps),
                comentario_ia=texto_do_form, # Campo que armazena o texto
                sentimento=sentimento_detectado
            )

            for pergunta in perguntas:
                valor_resposta = request.POST.get(f'pergunta_{pergunta.id}')
                if valor_resposta:
                    tipo_pergunta = str(pergunta.tipo).upper()
                    if tipo_pergunta == 'NOTA':
                        RespostaPergunta.objects.create(
                            resposta_clima=resposta_pai,
                            pergunta=pergunta,
                            resposta_nota=int(valor_resposta)
                        )
                    else:
                        RespostaPergunta.objects.create(
                            resposta_clima=resposta_pai,
                            pergunta=pergunta,
                            resposta_texto=valor_resposta
                        )

            return render(request, 'clima/sucesso_clima.html')

    return render(request, 'clima/responder_pesquisa.html', {
        'pesquisa': pesquisa,
        'setores': setores,
        'perguntas': perguntas
    })

@login_required
def ver_resultados_pesquisa(request, pesquisa_id):
    if not request.user.is_superuser:
        return redirect('dashboard')

    pesquisa = get_object_or_404(PesquisaClima, id=pesquisa_id)
    # Importante: certifique-se que o campo de data no model é 'data_envio' ou 'data_criacao'
    # Se o seu model usa 'data_criacao', ajuste abaixo para .order_by('-data_criacao')
    respostas = RespostaClima.objects.filter(pesquisa=pesquisa).order_by('-id')
    
    total_respostas = respostas.count()
    media_nota = respostas.aggregate(Avg('nota_enps'))['nota_enps__avg'] or 0

    promotores = respostas.filter(nota_enps__gte=9).count()
    detratores = respostas.filter(nota_enps__lte=6).count()
    neutros = respostas.filter(nota_enps__in=[7, 8]).count()
    
    enps_score = 0
    if total_respostas > 0:
        enps_score = ((promotores - detratores) / total_respostas) * 100

    # Dicionário de distribuição para o gráfico de barras
    distribuicao = {f"nota_{i}": respostas.filter(nota_enps=i).count() for i in range(11)}

    # Lógica para o Gráfico de Radar (Média por Setor)
    medias_por_setor = respostas.values('setor__nome').annotate(media=Avg('nota_enps'))
    labels_radar = [s['setor__nome'] for s in medias_por_setor if s['setor__nome']]
    valores_radar = [round(s['media'], 1) for s in medias_por_setor if s['setor__nome']]

    context = {
        'pesquisa': pesquisa,
        'respostas': respostas,
        'media_nota': round(media_nota, 1),
        'enps_score': round(enps_score, 1),
        'total_respostas': total_respostas,
        'promotores_count': promotores,
        'detratores_count': detratores,
        'neutros_count': neutros,
        'labels_radar': labels_radar,
        'valores_radar': valores_radar,
        **distribuicao 
    }
    return render(request, 'clima/resultados_pesquisa.html', context)

@login_required
def editar_pesquisa(request, pesquisa_id):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    pesquisa = get_object_or_404(PesquisaClima, id=pesquisa_id)
    
    if request.method == "POST":
        pesquisa.titulo = request.POST.get('titulo')
        pesquisa.descricao = request.POST.get('descricao')
        pesquisa.ativa = 'ativa' in request.POST 
        pesquisa.save()
        messages.success(request, f"Pesquisa '{pesquisa.titulo}' atualizada com sucesso!")
        return redirect('gerenciar_pesquisas')
        
    return render(request, 'clima/editar_pesquisa.html', {'pesquisa': pesquisa})

@login_required
def excluir_pesquisa(request, pesquisa_id):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    pesquisa = get_object_or_404(PesquisaClima, id=pesquisa_id)
    
    if request.method == "POST":
        titulo = pesquisa.titulo
        pesquisa.delete()
        messages.success(request, f"Pesquisa '{titulo}' removida com sucesso!")
        return redirect('gerenciar_pesquisas')
        
    return render(request, 'clima/confirmar_exclusao.html', {'pesquisa': pesquisa})