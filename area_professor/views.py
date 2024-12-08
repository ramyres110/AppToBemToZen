from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Simulados, SimuladoQuestao, Turmas, Questoes, RespostaSimulado, TurmaAluno

GRUPO_ALUNOS = 'grupo_alunos'
GRUPO_PROFESSORES = 'grupo_professores'
GRUPO_ADMINS = 'grupo_administradores'

MENU = [
    {
        "titulo":"Simulados",
        "link":"area_professor_simulados"
    },
    {
        "titulo":"Banco de Questões",
        "link":"area_professor_questoes"
    },
    {
        "titulo":"Turmas",
        "link":"area_professor_turmas"
    },
    {
        "titulo":"Alunos",
        "link":"area_professor_alunos"
    },
    {
        "titulo":"Forum",
        "link":"forum"
    }
]

def obter_perfil(user):
    perfil = ""
    if user.groups.filter(name=GRUPO_ADMINS).exists():
        perfil = 'ADMINISTRADOR'
    elif user.groups.filter(name=GRUPO_PROFESSORES).exists():
        perfil = 'PROFESSOR'
    return perfil

@login_required
def area_professor_index(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')

    qtd_simulados = Simulados.objects.filter(professor = request.user).count()
    qtd_questoes = Questoes.objects.filter(professor = request.user).count()

    turmas = Turmas.objects.filter(professor = request.user)

    #qtd_respostas_forum = Simulados.objects.filter(professor = request.user).count()
    qtd_respostas = RespostaSimulado.objects.filter(turma__in = turmas).count()
    qtd_alunos = TurmaAluno.objects.filter(turma__in = turmas).count()

    return render(request, 'area_professor/index.html', {
        "perfil": perfil,
        "menu": MENU,
        "qtd_simulados": qtd_simulados,
        "qtd_turmas": len(turmas),
        "qtd_alunos": qtd_alunos,
        "qtd_questoes": qtd_questoes,
        "qtd_respostas": qtd_respostas,
        "qtd_respostas_forum": 0,
    })

### SIMULADOS ###############################################
@login_required
def area_professor_simulados(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    cabecalhos = {
        "id":"#",
        "descricao": "Descrição",
        "turma_id": "Turma",
        "data_inicio": "Dt. Inicio",
        "data_fim": "Dt. Final",
    }
    
    simulados = Simulados.objects.filter(professor = request.user).values()
    
    return render(request, "area_professor/lista.html",{
        "perfil": perfil,
        "menu": MENU,
        "cabecalhos": cabecalhos,
        "dados": simulados,
        "edit_link": "area_professor_simulado",
        "novo_link": "area_professor_cad_simulados"
    })

### SIMULADOS
@login_required
def area_professor_simulado(request, id):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    try:
        simulado = Simulados.objects.get(id = id)
    except:
        return HttpResponse('Not Found', status=404)

    return render(request, "area_professor/base.html",{
        "perfil": perfil,
        "menu": MENU,
        "dado": simulado
    })

### SIMULADOS
@login_required
def area_professor_cad_simulados(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    turmas = Turmas.objects.filter(professor = request.user)
    questoes = Questoes.objects.filter(professor = request.user)

    contexto = {
        "perfil": perfil,
        "menu": MENU,
        "turmas": turmas,
        "questoes": questoes
    }
    
    if request.method == "POST":        
        descricao = request.POST["descricao"]
        turma_id = request.POST["turma"]
        dt_inicio = request.POST["dt_inicio"]
        dt_fim = request.POST["dt_fim"]
        questoesselecionadas = request.POST["questoesselecionadas"]

        if not questoesselecionadas:
            contexto["error"] = "Selecione as questões"
            return render(request, "area_professor/form_simulado.html", contexto)

        turma = Turmas.objects.get(id=turma_id) 

        simulado = Simulados.objects.create(
            descricao=descricao,
            turma=turma,
            professor=request.user
        )
        if dt_inicio:
            simulado.dt_inicio = dt_inicio
        if dt_fim:
            simulado.dt_fim = dt_fim
        simulado.save()

        questoes_lista = questoesselecionadas.split(",")
        for questao_id in questoes_lista:
            questao = Questoes.objects.get(id=questao_id)
            SimuladoQuestao.objects.create(
                simulado=simulado,
                questao=questao
            ).save()

        return redirect("area_professor_simulados")

    return render(request, "area_professor/form_simulado.html", contexto)


### TURMAS ###############################################
@login_required
def area_professor_turmas(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    cabecalhos = {
        "id":"#",
        "ano": "Ano",
        "escola": "Escola",
        "serie": "Serie",
        "turno": "Turno",
    }
    
    turmas = Turmas.objects.filter(professor = request.user).values()
    
    return render(request, "area_professor/lista.html",{
        "perfil": perfil,
        "menu": MENU,
        "cabecalhos": cabecalhos,
        "dados": turmas,
        "edit_link": "area_professor_turma",
        "novo_link": "area_professor_cad_turmas"
    })

### TURMAS
@login_required
def area_professor_turma(request, id):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    try:
        turma = Turmas.objects.get(id = id)
    except:
        return HttpResponse('Not Found', status=404)
    
    return render(request, "area_professor/base.html",{
        "perfil": perfil,
        "menu": MENU,
        "dado": turma
    })

### TURMAS
@login_required
def area_professor_cad_turmas(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    if request.method == "POST":
        escola = request.POST["escola"]
        serie = request.POST["serie"]
        turno = request.POST["turno"]
        ano = request.POST["ano"]
        professor  = request.user
        Turmas.objects.create(
            escola=escola,
            serie=serie,
            turno=turno,
            ano=ano,
            professor=professor
        ).save()

        return redirect("area_professor_turmas")
    
    return render(request, "area_professor/form_turma.html",{
        "perfil": perfil,
        "menu": MENU,
    })


### ALUNOS ###############################################
@login_required
def area_professor_alunos(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    cabecalhos = {
        "id":"#",
        "first_name": "Nome",
        "last_name": "Sobrenome",
        "email": "email",
    }

    turmas = Turmas.objects.filter(professor = request.user)
    turmaAlunos = TurmaAluno.objects.filter(turma__in = turmas).values_list("aluno_id")
    alunos = User.objects.filter(id__in = turmaAlunos).values()
    
    return render(request, "area_professor/lista.html",{
        "perfil": perfil,
        "menu": MENU,
        "cabecalhos": cabecalhos,
        "dados": alunos,
        "edit_link": "area_professor_aluno",
        "novo_link": "area_professor_cad_alunos"
    })

### ALUNOS
@login_required
def area_professor_aluno(request, id):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    try:
        aluno = User.objects.get(id = id)
    except:
        return HttpResponse('Not Found', status=404)
    
    return render(request, "area_professor/base.html",{
        "perfil": perfil,
        "menu": MENU,
        "dado": aluno
    })

### ALUNOS
@login_required
def area_professor_cad_alunos(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    return render(request, "area_professor/base.html",{
        "perfil": perfil,
        "menu": MENU,
    })


### QUESTOES ###############################################
@login_required
def area_professor_questoes(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    cabecalhos = {
        "id":"#",
        "descricao": "Descrição",
        "area_conhecimento": "Área do conhecimento",
        "valor": "Valor",
    }

    questoes = Questoes.objects.filter(professor = request.user).values()
    
    return render(request, "area_professor/lista.html",{
        "perfil": perfil,
        "menu": MENU,
        "cabecalhos": cabecalhos,
        "dados": questoes,
        "edit_link": "area_professor_questao",
        "novo_link": "area_professor_cad_questoes"
    })

### QUESTOES
@login_required
def area_professor_questao(request, id):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    return render(request, "area_professor/base.html",{
        "perfil": perfil,
        "menu": MENU,
    })

### QUESTOES
@login_required
def area_professor_cad_questoes(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    return render(request, "area_professor/base.html",{
        "perfil": perfil,
        "menu": MENU,
    })


### RESPOSTAS ###############################################
@login_required
def area_professor_respostas(request):
    perfil = obter_perfil(request.user);
    if perfil == "":
        return redirect('area_aluno_index')
    
    return render(request, "area_professor/base.html",{
        "perfil": perfil,
        "menu": MENU,
    })
