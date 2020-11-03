from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


class Comentario(models.Model):
    nome = models.CharField(max_length=191)
    email = models.EmailField()
    comentario = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    data = models.DateTimeField(default=timezone.now)
    publicado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
