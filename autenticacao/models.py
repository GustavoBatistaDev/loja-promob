from django.db import models
from datetime import datetime
from django.contrib.auth.models import User



class Token(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    validade = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username
