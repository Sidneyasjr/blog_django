import os

from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.conf import settings


class Post(models.Model):
    titulo = models.CharField(max_length=191)
    autor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data = models.DateTimeField(default=timezone.now)
    conteudo = models.TextField()
    excerto = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, blank=True, null=True)
    imagem = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True)
    publicado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.resize_image(self.imagem, 800)

    @staticmethod
    def resize_image(image_name, new_width):
        img_path = os.path.join(settings.MEDIA_ROOT, image_name)
        img = Image.open(img_path)
        width, height = img.size
        new_height = round((new_width * height) / width)

        if width <= new_width:
            img.close()
            return

        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(img_path, optimize=True, quality=60)
        new_img.close()
