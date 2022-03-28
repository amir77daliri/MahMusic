from django.shortcuts import render, get_object_or_404
from .models import Music
from Singer.models import Singer
from Album.models import Album
from django.views.generic import ListView, DetailView

# Home page
def home(request):
    new_songs = Music.objects.filter(status='A')[:11]
    singers = Singer.objects.all()[:14]
    albums = Album.objects.all()[:11]

    # just for test in start, complete later :
    most_rated = new_songs[:6]

    context = {
        'new_songs': new_songs,
        'singers': singers,
        'albums': albums,
        'most_rated': most_rated
    }

    return render(request, 'home-page/home.html', context)


class MusicList(ListView):
    model = Music
    template_name = 'Music/music-list.html'
    paginate_by = 24
    context_object_name = 'songs'


class MusicDetail(DetailView):
    model = Music
    template_name = 'Music/music-detail.html'
    context_object_name = 'music'

    def get_object(self, **kwargs):
        global slug
        global music
        slug = self.kwargs.get('slug')
        music = get_object_or_404(Music, slug=slug)
        return music

    def get_context_data(self, **kwargs):
        context = super(MusicDetail, self).get_context_data(**kwargs)
        context['related_list'] = Music.objects.get_related_songs_with(music)
        return context
