from django.db import models
from django.contrib.auth.models import User

class Turmas(models.Model):
    escola = models.CharField(max_length=150)
    serie = models.CharField(max_length=50)
    TIPO_TURNO = {
        "M": "Matutino",
        "V": "Vespertino",
        "N": "Noturno",
    }
    turno = models.CharField(
        max_length=1,
        choices=TIPO_TURNO
    )
    ano = models.SmallIntegerField()
    professor = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.escola} - {self.ano} - {self.TIPO_TURNO.get(self.turno)} - {self.serie}"


class TurmaAluno(models.Model):
    turma = models.ForeignKey(Turmas, on_delete=models.PROTECT)
    aluno = models.ForeignKey(User, on_delete=models.PROTECT, related_name='aluno')

    def __str__(self):
        return f"{self.turma} - {self.aluno.first_name} {self.aluno.last_name}"


class Questoes(models.Model):
    descricao = models.TextField()
    explicacao = models.TextField(null=True, blank=True)
    professor = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    AREAS_CONHECIMENTO = {
        'H': 'Ciências Humanas e suas Tecnologias',
        'L': 'Linguagens, Códigos e suas Tecnologias',
        'B': 'Ciências da Natureza e suas Tecnologias',
        'E': 'Matemática e suas Tecnologias',
    }
    area_conhecimento = models.CharField(
        max_length=1,
        choices=AREAS_CONHECIMENTO
    )
    valor = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.id} - {self.AREAS_CONHECIMENTO.get(self.area_conhecimento)} - {self.descricao}"


class Opcoes(models.Model):
    questao = models.ForeignKey(Questoes, on_delete=models.PROTECT)
    descricao = models.TextField()
    opcao_correta = models.BooleanField(default=False)
    explicacao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.questao.id} - {self.descricao} = {self.opcao_correta}"


class Simulados(models.Model):
    descricao = models.TextField(max_length=150)
    professor = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    turma = models.ForeignKey(Turmas, on_delete=models.PROTECT, null=True)
    data_inicio = models.DateField(null=True)
    data_fim = models.DateField(null=True)

    def __str__(self):
        return self.descricao


class SimuladoQuestao(models.Model):
    simulado = models.ForeignKey(Simulados, on_delete=models.PROTECT)
    questao = models.ForeignKey(Questoes, on_delete=models.PROTECT)

    def __str__(self):
        return F"{self.simulado.id} - {self.simulado.descricao} = {self.questao}"


class RespostaSimulado(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.PROTECT)
    turma = models.ForeignKey(Turmas, on_delete=models.PROTECT, null=True, blank=True)
    simulado = models.ForeignKey(Simulados, on_delete=models.PROTECT)
    questao = models.ForeignKey(Questoes, on_delete=models.PROTECT)
    opcao = models.ForeignKey(Opcoes, on_delete=models.PROTECT)
    acertou = models.BooleanField(default=False)

    # TODO: Criar metodo mágico ToString
    # Deve retornar aluno.first_name - turma.id - questa.descricao - opcao.descricao - acertou
