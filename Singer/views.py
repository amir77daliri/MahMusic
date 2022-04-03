from django.shortcuts import render, get_object_or_404
from .models import Singer
from Music.models import Music
from django.views.generic import ListView, DetailView


class SingerList(ListView):
    model = Singer
    template_name = 'Singer/singer-list.html'
    paginate_by = 24
    context_object_name = 'singers'

    def get_queryset(self):
        singers = Singer.objects.all().order_by('name')
        return singers

class SingerDetail(DetailView):
    model = Singer
    template_name = 'Singer/singer-detail.html'
    context_object_name = 'singer'

    def get_object(self, **kwargs):
        global slug
        global singer
        slug = self.kwargs.get('slug')
        singer = get_object_or_404(Singer, slug=slug)
        return singer

    def get_context_data(self, **kwargs):
        context = super(SingerDetail, self).get_context_data(**kwargs)
        context['related_list'] = Singer.objects.exclude(slug=slug)[:12]
        context['singer_musics'] = singer.musics.all()
        context['singer_albums'] = singer.albums.all()
        return context
