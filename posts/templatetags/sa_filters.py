from django import template

register = template.Library()


@register.filter(name='plural_comentarios')
def plural_comentarios(num_comentarios):
    try:
        num_comentarios = int(num_comentarios)

        if num_comentarios == 0:
            return f'Nenhum Comentario'
        elif num_comentarios == 1:
            return f'{num_comentarios} Comentario'
        else:
            return f'{num_comentarios} Comentarios'
    except:
        return f'{num_comentarios} Comentario(s)'
