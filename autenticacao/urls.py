from django.urls import path
from . import views


urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
    path('login/', views.login, name="login"),
    path('ativacao/<str:token>', views.ativacao, name='ativacao'),
    path('sair/', views.sair, name='sair'),

]