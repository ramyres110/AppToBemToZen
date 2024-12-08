from django.contrib import admin

from . import models

admin.site.register(models.Turmas);
admin.site.register(models.TurmaAluno);
admin.site.register(models.Simulados);
admin.site.register(models.SimuladoQuestao);
admin.site.register(models.Questoes);
admin.site.register(models.Opcoes);
admin.site.register(models.RespostaSimulado);
