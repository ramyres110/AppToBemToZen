from django.urls import path

from . import views as area_professor

urlpatterns = [
    path('', area_professor.area_professor_index, name="area_professor_index"),

    path('simulados', area_professor.area_professor_simulados, name="area_professor_simulados"),
    path('simulado/<int:id>', area_professor.area_professor_simulado, name="area_professor_simulado"),
    path('cadastro/simulado', area_professor.area_professor_cad_simulados, name="area_professor_cad_simulados"),
    
    path('turmas', area_professor.area_professor_turmas, name="area_professor_turmas"),
    path('turma/<int:id>', area_professor.area_professor_turma, name="area_professor_turma"),
    path('cadastro/turma', area_professor.area_professor_cad_turmas, name="area_professor_cad_turmas"),
    
    path('alunos', area_professor.area_professor_alunos, name="area_professor_alunos"),
    path('aluno/<int:id>', area_professor.area_professor_aluno, name="area_professor_aluno"),
    path('cadastro/aluno', area_professor.area_professor_cad_alunos, name="area_professor_cad_alunos"),
    
    path('questoes', area_professor.area_professor_questoes, name="area_professor_questoes"),
    path('questao/<int:id>', area_professor.area_professor_questao, name="area_professor_questao"),
    path('cadastro/questao', area_professor.area_professor_cad_questoes, name="area_professor_cad_questoes"),

    path('respostas', area_professor.area_professor_respostas, name="area_professor_respostas"),
]