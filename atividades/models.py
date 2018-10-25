from django.db import models
from django.contrib.auth.models import User

class Turma(models.Model):
    nome = models.CharField(max_length=256)
    codigo = models.CharField(max_length=5, unique=True)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'


    def __str__(self):
        return self.nome


class Aluno_em_Turma(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)


class Atividade(models.Model):
    disciplina = models.CharField(max_length=256, null=True)
    nome = models.CharField(max_length=256)
    entrega = models.DateField()
    nota = models.CharField(max_length=256)
    obs = models.TextField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    criador = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
