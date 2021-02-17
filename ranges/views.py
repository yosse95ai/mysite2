from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse

from .models import Range, Artist, Song, Note


def index(request):
    pub_list = Range.objects.order_by('-pub_date')[:10]
    release_list = Range.objects.order_by('-release_date')[:10]
    context = {
        'pub_list': pub_list,
        'release_list': release_list
    }
    return render(request, 'ranges/index.html', context)


def queryError(error_name, input_name=None):
    return {error_name: True, 'input_name': input_name}


def detail(request, artist_pk, song_pk):
    try:
        artist = get_object_or_404(Artist, pk=artist_pk)
        song = get_object_or_404(Song, pk=song_pk)
        target = get_object_or_404(Range, song=song, artist=artist)
        lowest_note = get_object_or_404(Note, pk=target.lowest_note.pk)
        highest_note = get_object_or_404(Note, pk=target.highest_note.pk)
    except Artist.DoesNotExist:
        context = queryError('artist_error')
    except Song.DoesNotExist:
        context = queryError('song_error')
    except Range.DoesNotExist:
        context = queryError('range_error')
    except Note.DoesNotExist:
        context = queryError('note_error')
    else:
        song_name = song.song_name
        composers = song.composer.all()
        lyricists = song.lyricist.all()
        arrangers = song.arranger.all()
        performers = target.performer.all()
        release = target.release_date
        genre = target.genre
        context = {
            'artist': artist,
            'song': song_name,
            'composers': composers,
            'lyricists': lyricists,
            'arrangers': arrangers,
            'highest_note': highest_note,
            'lowest_note': lowest_note,
            'target': target,
            'performers': performers,
            'genre': genre,
            'release': release,
        }
    return render(request, 'ranges/detail.html', context)


def search(request):
    content = {}
    return render(request, 'ranges/search.html', content)


def result(request):
    input_name = request.POST['song_name']
    results = list()
    songs = Song.objects.filter(song_name=input_name)
    if not songs:
        context = queryError('song_error', input_name=input_name)
    else:
        for song in songs:
            try:
                result = get_list_or_404(Range, song=song.pk)
            except Range.DoesNotExist:
                context = queryError('range_error', input_name=input_name)
            else:
                results += result
                context = {
                    'results': results,
                    'input_name': input_name,
                }
    return render(request, 'ranges/result.html', context)


def result_renge(request, note_pk):
    high_ranges = Range.objects.filter(highest_note=note_pk)
    low_ranges = Range.objects.filter(lowest_note=note_pk)
    if not high_ranges and not low_ranges:
        context=queryError('range_note_error')
    else:
        context = {
            'high_ranges': high_ranges,
            'low_ranges': low_ranges,
            'input_name': get_object_or_404(Note, pk=note_pk).note_name,
            'h_num': Range.objects.filter(highest_note=note_pk).count(),
            'l_num': Range.objects.filter(lowest_note=note_pk).count(),
        }
    return render(request, 'ranges/result.html', context)
