import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .common.decorators import ajax_required
from .models import Music, MusicViewsHit, PlayList
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
        ip_address = self.request.user.ip_address
        if ip_address not in music.hits.all():
            MusicViewsHit.objects.create(ip_address=ip_address, music=music)
        return music

    def get_context_data(self, **kwargs):
        context = super(MusicDetail, self).get_context_data(**kwargs)
        context['related_list'] = Music.objects.get_related_songs_with(music)
        return context


@ajax_required
@require_POST
def like_music(request):
    if request.user.is_authenticated:
        music_id = request.POST.get('id')
        action = request.POST.get('action')
        if music_id and action:
            try:
                music = get_object_or_404(Music, id=music_id)
                if action == 'like':
                    music.users_like.add(request.user)
                    return JsonResponse({'status': 'add'})
                else:
                    music.users_like.remove(request.user)
                    return JsonResponse({'status': 'remove'})
            except:
                pass
        return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'not authorize'})


@ajax_required
@require_POST
def add_to_playlist(request):
    if request.user.is_authenticated:
        music_id = request.POST.get('id')
        action = request.POST.get('action')
        if music_id and action:
            try:
                music = get_object_or_404(Music, id=music_id)
                if action == 'save':
                    music.user_playlist.add(request.user)
                    return JsonResponse({'status': 'save'})
                else:
                    music.user_playlist.remove(request.user)
                    return JsonResponse({'status': 'remove'})
            except:
                pass
        return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'not authorize'})


@ajax_required
@require_POST
def del_from_favorite(request):
    if request.user.is_authenticated:
        data = request.POST.get('data')
        data = json.loads(data)
        for i in data:
            music_id = int(i['id'])
            try:
                music = get_object_or_404(Music, id=music_id)
                music.users_like.remove(request.user)
            except:
                pass

    return JsonResponse({'data': 'ok'})


@ajax_required
@require_POST
def del_from_playlist(request):
    if request.user.is_authenticated:
        data = request.POST.get('data')
        data = json.loads(data)
        for i in data:
            music_id = int(i['id'])
            try:
                music = get_object_or_404(Music, id=music_id)
                music.user_playlist.remove(request.user)
            except:
                pass

    return JsonResponse({'data': 'ok'})
