from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from posts.models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('categoria')
        qs = qs.order_by('-data').filter(publicado=True)
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado=True, then=1)
                )
            )
        )

        return qs


class PostBusca(PostIndex):
    template_name = 'posts/busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo__icontains=termo) |
            Q(autor__username__iexact=termo) |
            Q(data__icontains=termo) |
            Q(conteudo__icontains=termo) |
            Q(excerto__icontains=termo) |
            Q(categoria__nome__iexact=termo)
        )

        return qs


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()

        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs
        qs = qs.filter(categoria__nome__iexact=categoria)

        return qs


class PostDetalhes(UpdateView):
    template_name = 'posts/post_detalhes.html'
    model = Post
    form_class = FormComentario
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentario.objects.filter(publicado=True, post=post.id)
        contexto['comentarios'] = comentarios

        return contexto

    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentario(**form.cleaned_data)
        comentario.post = post

        if self.request.user.is_authenticated:
            comentario.usuario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentario enviado com sucesso.')
        return redirect('post_detalhes', pk=post.id)
