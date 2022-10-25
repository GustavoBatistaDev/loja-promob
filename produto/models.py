from statistics import mode
from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe


class Imagens(models.Model):
    file = models.FileField(upload_to='imagens')
    def __str__(self) :
        return self.file.url


class Categoria(models.Model):
    categoria = models.CharField(max_length=200)

    def __str__(self):
        return self.categoria

class Produto(models.Model):
    nome_produto = models.CharField(max_length=500)
    img = models.ImageField(upload_to='post_img')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    preco = models.FloatField()
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    files = models.ManyToManyField(Imagens, blank=True)

    def __str__(self):
        return self.nome_produto
