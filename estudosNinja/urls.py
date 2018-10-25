"""
estudosNinja URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from atividades import views
from comments import views as comment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginAluno.as_view(), name='login'),
    path('cadastro/', views.SignUp.as_view(), name='cadastro'),
    path('criar-turma/', views.CriarTurmaView.as_view(), name='criar-turma'),
    path('logout/', auth_views.LogoutView.as_view(),
         {'next_page': '/'}, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<slug:uidb64>/<slug:token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('e/<str:codigo>/', views.adicionar_aluno, name='adicionar-aluno'),
    path('entrar/', views.EntrarTurmaView.as_view(), name='entrar-turma'),
    path('turmas/', views.TurmasView.as_view(), name='ver-turmas'),
    path('v/<str:codigo>/', views.VerTurmaView.as_view(), name='ver-turma'),
    path('v/<str:codigo_turma>/criar/',
         views.CriarAtividadeView.as_view(), name='criar-atividade'),
    path('v/<str:codigo_turma>/a/<int:ak>',
         views.VerAtividadeView.as_view(), name='ver-atividade'),
    path('v/<str:codigo_turma>/a/<int:ak>/editar',
         views.editar_atividade, name='editar-atividade'),
    path('sair/', views.sair, name='sair'),
    path('comments/', include('django_comments.urls')),
    path('postar/', comment_views.post_comment, name='postar-comentario')
]
