from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse

from .models import Range, Artist, Song, Note


def index(request):
    all_range_list = Range.objects.all()
    context = {'all_range_list': all_range_list}
    return render(request, 'ranges/index.html', context)


def detail(request, artist_pk, song_pk):
    artist = Artist.objects.get(pk=artist_pk)
    artist_name = Artist.objects.get(pk=artist_pk)
    song = Song.objects.get(pk=song_pk)
    song_name=song.song_name
    composers = song.composer.all()
    lyricists = song.lyricist.all()
    target = Range.objects.get(song=song, artist=artist)
    lowest_note = Note.objects.get(pk=target.lowest_note.pk)
    highest_note = Note.objects.get(pk=target.highest_note.pk)
    performers = target.performer.all()
    release = target.release_date
    genre=target.genre
    context = {
        'artist': artist_name,
        'song': song_name,
        'composers': composers,
        'lyricists': lyricists,
        'highest_note': highest_note,
        'lowest_note': lowest_note,
        'target': target,
        'performers': performers,
        'genre': genre,
        'release':release,
        }
    return render(request, 'ranges/detail.html', context)
