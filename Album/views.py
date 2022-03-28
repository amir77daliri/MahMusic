from django.shortcuts import render, get_object_or_404
from .models import Album
from Music.models import Music
from django.views.generic import ListView, DetailView


class AlbumList(ListView):
    model = Album
    template_name = 'Album/album-list.html'
    paginate_by = 24
    context_object_name = 'albums'


class AlbumDetail(DetailView):
    model = Album
    template_name = 'Album/album-detail.html'
    context_object_name = 'album'

    def get_object(self, **kwargs):
        global slug
        global album
        slug = self.kwargs.get('slug')
        album = get_object_or_404(Album, slug=slug)
        return album

    def get_context_data(self, **kwargs):
        pass
