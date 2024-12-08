from django.urls import path

from . import views as area_aluno

urlpatterns = [
    path('', area_aluno.area_aluno_index, name="area_aluno_index"),
    path('simulados/', area_aluno.area_aluno_simulados, name="area_aluno_simulados"),
    path('simulados/<int:id_simulado>/responder', area_aluno.area_aluno_responder, name="area_aluno_responder"),
    path('turmas/', area_aluno.area_aluno_turma, name="area_aluno_turma"),
    path('respostas/', area_aluno.area_aluno_respostas, name="area_aluno_respostas"),
]