import string
import random
from datetime import datetime, date

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import login, logout, authenticate, views as auth_views
from django.views.generic import FormView, TemplateView, ListView, RedirectView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from atividades.forms import SignUpForm, LogInForm, CriarTurmaForm, CriarAtividadeForm, EntrarTurmaForm
from atividades.models import Aluno_em_Turma, Turma, Atividade

# Create your views here.


class SignUp(FormView):
    template_name = 'atividades/cadastro.html'
    form_class = SignUpForm
    success_url = reverse_lazy('ver-turmas')

    def form_valid(self, form):
        aluno = form.save(commit=False)
        aluno.email = form.cleaned_data['username']
        aluno.save()
        user = authenticate(
            username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return redirect('ver-turmas')

    def form_invalid(self, form):
        messages.error(
            self.request, "Por favor, preencha corretamente os campos")
        return self.render_to_response(self.get_context_data(form=form))


class LoginAluno(FormView):
    template_name = 'atividades/login.html'
    form_class = LogInForm
    success_url = reverse_lazy('ver-turmas')

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('ver-turmas')
        return super(LoginAluno, self).get(request)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect('ver-turmas')

        return render(request, 'atividades/login.html', {'form': self.get_form()})


@login_required
def adicionar_aluno(request, codigo):
    if request.user.is_authenticated:
        if testar_codigo(codigo):
            checar_atividades(codigo)
            q = Aluno_em_Turma.objects.filter(
                id_usuario=request.user, turma=Turma.objects.get(codigo__exact=codigo))
            if q.exists():
                return redirect('ver-turma', codigo=codigo)
            else:
                a = Aluno_em_Turma.objects.create(
                    id_usuario=request.user, turma=Turma.objects.get(codigo__exact=codigo))
                a.save()
                print('adicionado')
                return redirect('ver-turma', codigo=codigo)
    return render(request, 'atividades/entrar_falhou.html')


class CriarTurmaView(LoginRequiredMixin, FormView):
    template_name = 'atividades/criar_turma.html'
    form_class = CriarTurmaForm

    def post(self, request):
        nome = request.POST['nome']
        codigo = gerar_codigo()
        t = Turma.objects.create(nome=nome, codigo=codigo)
        return redirect('adicionar-aluno', codigo=codigo)


class EntrarTurmaView(LoginRequiredMixin, FormView):
    template_name = 'atividades/entrar_turma.html'
    form_class = EntrarTurmaForm

    def post(self, request):
        codigo = request.POST['codigo']
        checar_atividades(codigo)
        return redirect('adicionar-aluno', codigo=codigo)


@login_required
def sair(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


class VerTurmaView(LoginRequiredMixin, ListView):
    template_name = 'atividades/ver_turma.html'

    def get_context_data(self, **kwargs):
        context = super(VerTurmaView, self).get_context_data(**kwargs)
        turma = Turma.objects.get(codigo=self.kwargs['codigo'])
        print(self.kwargs['codigo'])
        context['turma'] = turma
        return context

    def get_queryset(self):
        codigo = self.kwargs['codigo']
        checar_atividades(codigo)
        turma = Turma.objects.get(codigo=codigo)
        print(turma)
        queryset = Atividade.objects.filter(turma=turma)
        return queryset


class TurmasView(LoginRequiredMixin, ListView):
    template_name = 'atividades/turmas.html'

    def get_queryset(self):
        user = self.request.user
        return Aluno_em_Turma.objects.filter(id_usuario=user)


class CriarAtividadeView(LoginRequiredMixin, FormView):
    template_name = 'atividades/criar_atividade.html'
    form_class = CriarAtividadeForm

    def post(self, request, codigo_turma):
        checar_atividades(codigo_turma)
        disciplina = request.POST['disciplina']
        nome = request.POST['nome']
        data = request.POST['entrega']
        entrega = datetime.strptime(data, "%Y-%m-%d").date()
        nota = request.POST['nota']
        obs = request.POST['obs']
        turma = Turma.objects.get(codigo=codigo_turma)
        user = request.user
        a = Atividade.objects.create(disciplina=disciplina, nome=nome,
                                     entrega=entrega, nota=nota, obs=obs, turma=turma, criador=user)
        return redirect('ver-atividade', codigo_turma=turma.codigo, ak=a.id)


def editar_atividade(request, codigo_turma, ak):
    if request.method == 'GET':
        atividade = Atividade.objects.get(id=ak)
        form = CriarAtividadeForm(initial={'disciplina': atividade.disciplina,
         'nome': atividade.nome, 'entrega': atividade.entrega, 'nota': atividade.nota, 'obs': atividade.obs})

    if request.method == 'POST':
        atividade = Atividade.objects.get(id=ak)
        form = CriarAtividadeForm(request.POST)
        if form.is_valid():
            atividade.id = ak
            atividade.disciplina = form.cleaned_data['disciplina']
            atividade.nome = form.cleaned_data['nome']
            data = form.cleaned_data['entrega']
            atividade.entrega = datetime.strptime(str(data), "%Y-%m-%d").date()
            atividade.nota = form.cleaned_data['nota']
            atividade.obs = form.cleaned_data['obs']
            atividade.save()
            return redirect('ver-atividade', codigo_turma=codigo_turma, ak=ak)

    return render(request, 'atividades/criar_atividade.html', {'form': form})


class VerAtividadeView(LoginRequiredMixin, TemplateView):
    template_name = 'atividades/atividade.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atividade'] = Atividade.objects.get(id=self.kwargs['ak'])
        context['turma'] = Turma.objects.get(
            codigo=self.kwargs['codigo_turma'])
        context['aluno'] = self.request.user
        checar_atividades(self.kwargs['codigo_turma'])
        return context


def testar_codigo(codigo):
    try:
        Turma.objects.get(codigo=codigo)
        return True
    except:
        return False


def gerar_codigo(size=5, chars=string.ascii_uppercase+string.ascii_lowercase+string.digits):
    codigo = ''.join(random.choice(chars) for x in range(size))
    if testar_codigo(codigo):
        codigo = gerar_codigo()
    return codigo


def checar_atividades(codigo_turma):
    q = Atividade.objects.filter(turma=Turma.objects.get(codigo=codigo_turma))
    for atividade in q:
        if atividade.entrega <= date.today():
            atividade.delete()
            print('atividade deletada')
