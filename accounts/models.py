from django.db import models
from django.contrib.auth.models import User
from setores.models import Setor

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True)
    is_master = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
