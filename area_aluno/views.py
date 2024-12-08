from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from area_professor.models import Simulados, SimuladoQuestao, Turmas, RespostaSimulado, TurmaAluno, Questoes, Opcoes

GRUPO_ALUNOS = 'grupo_alunos'
GRUPO_PROFESSORES = 'grupo_professores'
GRUPO_ADMINS = 'grupo_administradores'

MENU = [
    {
        "titulo":"Simulados",
        "link":"area_aluno_simulados"
    },    
    {
        "titulo":"Turmas",
        "link":"area_aluno_turma"
    },
    {
        "titulo":"Respostas",
        "link":"area_aluno_respostas"
    },    
    {
        "titulo":"Forum",
        "link":"forum"
    }
]

PERFIL = "ALUNO"

@login_required
def area_aluno_index(request):
    turmaAluno = TurmaAluno.objects.filter(aluno = request.user).values_list("turma_id")
    turmas = Turmas.objects.filter(id__in=turmaAluno)

    qtd_simulados = Simulados.objects.filter(turma__in=turmas).count()
    qtd_turmas = turmas.count()
    qtd_respostas = RespostaSimulado.objects.filter(aluno=request.user).count()
    qtd_respostas_forum = 0

    return render(request, 'area_aluno/index.html', {
        "perfil": PERFIL,
        "menu": MENU,
        "qtd_simulados": qtd_simulados,
        "qtd_turmas": qtd_turmas,
        "qtd_respostas": qtd_respostas,
        "qtd_respostas_forum": qtd_respostas_forum,
    })

@login_required
def area_aluno_simulados(request):
    cabecalhos = {
        "id":"#",
        "descricao": "Descrição",
        "turma_id": "Turma",
        "data_inicio": "Dt. Inicio",
        "data_fim": "Dt. Final",
    }
    
    turmaAluno = TurmaAluno.objects.filter(aluno = request.user).values_list("turma_id")
    turmas = Turmas.objects.filter(id__in=turmaAluno)
    simulados = Simulados.objects.filter(turma__in=turmas).values()

    return render(request, "area_professor/lista.html",{
        "perfil": PERFIL,
        "menu": MENU,
        "cabecalhos": cabecalhos,
        "dados": simulados,
        "acao_link": "area_aluno_responder"
    })

@login_required
def area_aluno_turma(request):
    cabecalhos = {
        "id":"#",
        "ano": "Ano",
        "escola": "Escola",
        "serie": "Serie",
        "turno": "Turno",
    }
    
    turmaAluno = TurmaAluno.objects.filter(aluno = request.user).values_list("turma_id")
    turmas = Turmas.objects.filter(id__in=turmaAluno).values()
    
    return render(request, "area_professor/lista.html",{
        "perfil": PERFIL,
        "menu": MENU,
        "cabecalhos": cabecalhos,
        "dados": turmas
    })

@login_required
def area_aluno_respostas(request):
    cabecalhos = {
        "id":"#",
        "simulado": "Simulado",
        "turma": "Turma",
        "questao": "Questão",
        "opcao": "Opção marcada",
        "acertou": "Acertou",
    }

    respostas = RespostaSimulado.objects.filter(aluno=request.user)

    respostas_formatadas = []
    for resposta in respostas:
        simulado = Simulados.objects.get(id=resposta.simulado_id)

        turma = ""
        try:
            turma = Turmas.objects.get(id=resposta.turma_id)
        except:
            pass
        
        questao = Questoes.objects.get(id=resposta.questao_id)
        opcao = Opcoes.objects.get(id=resposta.opcao_id)
        respostas_formatadas.append({
            "id": resposta.id,
            "simulado" : simulado,
            "turma" : turma,
            "questao" : questao.descricao,
            "opcao" : opcao.descricao,
            "acertou" : "SIM" if resposta.acertou else "NÃO",
        })

    return render(request, "area_professor/lista.html",{
        "perfil": PERFIL,
        "menu": MENU,
        "cabecalhos": cabecalhos,
        "dados": respostas_formatadas
    })

def area_aluno_responder(request, id_simulado):
    simulado = Simulados.objects.get(id=id_simulado)
    simulado_questao = SimuladoQuestao.objects.filter(simulado=simulado).values_list("questao_id")
    questoes = Questoes.objects.filter(id__in=simulado_questao)
    
    if request.method == "POST":        
        for questao_name, opcao_id in request.POST.items():
            if questao_name.startswith("opcao_"):
                questao_id = questao_name.split("_")[-1]
                aluno = request.user                
                questao = Questoes.objects.get(id=questao_id)
                opcao = Opcoes.objects.get(id=opcao_id)
                acertou = opcao.opcao_correta

                RespostaSimulado.objects.create(
                    aluno= aluno,
                    simulado= simulado,
                    questao= questao,
                    opcao= opcao,
                    acertou= acertou
                ).save()
        return redirect('area_aluno_respostas')

    
    questoes_formatadas = []
    for questao in questoes:
        opcoes = Opcoes.objects.filter(questao=questao).values()
        nova_questao = {
            "id": questao.id,
            "descricao": questao.descricao,
            "opcoes": opcoes
        }
        questoes_formatadas.append(nova_questao)

    return render(request, 'area_aluno/responder.html', {
        "perfil": PERFIL,
        "menu": MENU,
        "simulado": simulado,
        "questoes": questoes_formatadas
    })