from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('categoria/<int:categoria_id>', views.categoria, name='categoria'),
    path("produto/<int:id>", views.produto, name='produto'),
    path("add_carrinho/", views.add_carrinho, name='add_carrinho'),
    path("ver_carrinho/", views.ver_carrinho, name='ver_carrinho'),
    path("remover_carrinho/<int:session_id>", views.remover_carrinho, name='remover_carrinho'),
]