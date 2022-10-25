from django.contrib import admin
from .models import Categoria, Produto, Imagens



admin.site.register(Categoria)
admin.site.register(Imagens)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_produto', 'preco', 'ativo', 'categoria') 
    list_editable = ('preco', 'ativo')

