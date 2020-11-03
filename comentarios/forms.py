from django.forms import ModelForm
from .models import Comentario


class FormComentario(ModelForm):
    def clean(self):
        data = self.cleaned_data
        nome = data.get('nome')
        email = data.get('email')
        comentario = data.get('comentario')

        if len(nome) < 5:
            self.add_error(
                'nome',
                'Nome precisa ter mais que 5 caracteres.'
            )

    class Meta:
        model = Comentario
        fields = ('nome', 'email', 'comentario')
