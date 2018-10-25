from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Turma, Atividade

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput() )#attrs={'placeholder': 'Nome'}),max_length=30, required=True, help_text='*'
    last_name = forms.CharField(widget=forms.TextInput() )
    password1 = forms.CharField(widget=forms.PasswordInput()) #attrs={'placeholder':'Senha'}), required=True, min_length=8, max_length=16
    password2 = forms.CharField(widget=forms.PasswordInput() )#attrs={'placeholder':'Repita a Senha'}), required=True, min_length=8, max_length=16
    username = forms.EmailField(widget=forms.TextInput()) #attrs={'placeholder':'Email'}),max_length=254, help_text='Informe um Email válido', required=True



    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'username', 'password1', 'password2')


class LogInForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput()) #attrs={'placeholder':'Email'}),max_length=254, help_text='Informe um Email válido', required=True
    password = forms.CharField(widget=forms.PasswordInput()) #attrs={'placeholder' : 'Senha'}), required=True, min_length=8, max_length=16)
    class Meta:
        model = User
        fields = ('username', 'password')

class CriarTurmaForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput())#attrs={'placeholder':'Nome da Turma', 'class':'input_turma'}), max_length=256, help_text='Informe um nome para a turma', required=True)

    class Meta:
        model = Turma
        fields = ('nome')

class CriarAtividadeForm(forms.Form):
    disciplina = forms.CharField(widget=forms.TextInput())
    nome = forms.CharField(widget=forms.TextInput())
    entrega = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y', attrs={'type':'date'}))
    nota = forms.CharField(widget=forms.TextInput())
    obs = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'50' }))

    class Meta:
        model = Atividade
        fields = ('nome', 'entrega', 'nota', 'obs')

class EntrarTurmaForm(forms.Form):
    codigo = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Turma
        fields = ('codigo')