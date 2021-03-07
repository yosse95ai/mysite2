from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from datetime import datetime

from .models import Range, Artist, Song, Note, Genre
from .templatetags import noteBar as nb
from .forms import SongForm, ArtistForm, RangeForm


def queryError(error_name, input_name=None):
    return {error_name: True, 'input_name': input_name}


def paginate_query(request, queryset, count):
    '''
    ページネーション用に、Pageオブジェクトを返す。
    '''
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginatot.page(paginator.num_pages)
    return page_obj


def index(request):
    pub_list = Range.objects.order_by('-latest_update')[:10]
    release_list = Range.objects.order_by('-release_date')[:10]
    context = {
        'pub_list': pub_list,
        'release_list': release_list
    }
    return render(request, 'ranges/index.html', context)


def detail(request, artist_pk, song_pk, origin=''):
    '''
    responsed range-detail
    '''
    try:
        artist = Artist.objects.get(pk=artist_pk)
        song = Song.objects.get(pk=song_pk)
        target = Range.objects.get(song=song, artist=artist, origin=origin)
        lowest_note = Note.objects.get(pk=target.lowest_note.pk)
        highest_note = Note.objects.get(pk=target.highest_note.pk)
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
        release = target.release_date.strftime('%Y年%m月%d日')
        genre = target.genre
        is_original = target.origin
        context = {
            'artist_name': artist,
            'song_name': song_name,
            'composers': composers,
            'lyricists': lyricists,
            'arrangers': arrangers,
            'highest_note': highest_note,
            'lowest_note': lowest_note,
            'performers': performers,
            'genre_name': genre,
            'release': release,
            'is_original': is_original,
        }
        if target.fake_note:
            fake_note = Note.objects.get(pk=target.fake_note.pk)
            context['fake_note'] = fake_note
        if not is_original:
            this_key = nb.noteToNumber(highest_note.pk)
            try:
                origin = Range.objects.get(song=song_pk, origin=True)
            except Range.DoesNotExist:
                context['diffError'] = True
            else:
                origin_key = nb.noteToNumber(origin.highest_note.pk)
                context['diff'] = this_key-origin_key
    return render(request, 'ranges/detail.html', context)


def detail_artist(request, artist_pk):
    '''
    responsed artist-detail
    '''
    artist = Artist.objects.get(pk=artist_pk)
    artist_contents = Range.objects.filter(performer=artist)
    has_songs = Song.objects.filter(Q(composer=artist_pk) | Q(
        lyricist=artist_pk) | Q(arranger=artist_pk)).distinct()
    has_song_list = list()
    not_regist_list = list()
    for song in has_songs:
        try:
            s = Range.objects.get(song=song.pk, origin=True)
        except Range.DoesNotExist:
            not_regist_list.append(song)
        except Range.MultipleObjectsReturned:
            pass
        else:
            has_song_list.append(s)
    context = {
        'has_songs': has_songs,
        'contents': artist_contents,
        'input_name': artist,
        'has_song_list': has_song_list,
        'not_regist_list': not_regist_list,
    }
    return render(request, 'ranges/artist.html', context)


def search(request):
    '''
    search for song name
    '''
    notes_list = Note.objects.all()
    genres_list = Genre.objects.all()
    artists_list = Artist.objects.all()

    # アーティスト検索
    artist_list = list()
    for artist in artists_list:
        if Range.objects.filter(artist=artist):
            artist_list.append(artist)
    vocaloid = Artist.objects.filter(pk__startswith='V-')

    # 音域検索
    note_list = list()
    for note in notes_list:
        if Range.objects.filter(
        Q(highest_note=note.pk) | Q(lowest_note=note.pk) | Q(fake_note=note.pk)):
            note_list.append(nb.noteToNumber(note.pk))
    ordered_note = list()
    for note_n in sorted(note_list):
        pk = nb.numberToNote(note_n)
        ordered_note.append(notes_list.get(note_id=pk))

    # ジャンル検索
    genre_list = list()
    for genre in genres_list:
        if Range.objects.filter(genre=genre.pk):
            genre_list.append(genre)
    content = {
        'notes_list': ordered_note,
        'genre_list': genre_list,
        'artist_list': artist_list,
        'vcs': vocaloid,
    }
    return render(request, 'ranges/search.html', content)


def result(request, in_name=''):
    '''
    search for song-range
    大文字小文字区別なし検索
    かつ 文字列始まり検索
    '''
    if request.method == 'POST':
        input_name = request.POST['song_name']
    else:
        input_name = in_name
    results = list()
    songs = Song.objects.filter(
        song_name__istartswith=input_name).order_by('song_name')
    if not songs:
        context = queryError('song_error', input_name=input_name)
    else:
        for song in songs:
            result = Range.objects.filter(song=song.pk)
            if not result:
                context = queryError('range_error', input_name=input_name)
            else:
                results += result
        page_results = paginate_query(request, results, 10)
        context = {
            'results': page_results,
            'input_name': input_name,
        }
    return render(request, 'ranges/result.html', context)


def result_range(request, note_pk):
    '''
    search for registared note list
    '''
    ranges = Range.objects.filter(
        Q(highest_note=note_pk) | Q(lowest_note=note_pk) | Q(fake_note=note_pk)).order_by('highest_note')
    if not ranges:
        context = queryError('range_note_error',
                             input_name=Note.objects.get(pk=note_pk).note_name)
    else:
        note_ranges = paginate_query(request, ranges, 10)
        context = {
            'note_ranges': note_ranges,
            'input_name': Note.objects.get(pk=note_pk).note_name,
        }
    return render(request, 'ranges/result.html', context)


def result_genre(request, genre_pk):
    is_regist_genre = Range.objects.filter(
        genre=genre_pk).order_by('highest_note')
    if not is_regist_genre:
        context = queryError('genre_error')
    genre_list = paginate_query(request, is_regist_genre, 10)
    context = {
        'genre_list': genre_list,
        'input_name': Genre.objects.get(pk=genre_pk),
    }
    return render(request, 'ranges/result.html', context)


def result_all(request):
    all_cont = Range.objects.all().order_by('song', '-artist')
    all_cont_list = paginate_query(request, all_cont, 10)
    context = {
        'all_range': all_cont_list,
        'input_name': 'Search All'
    }
    return render(request, 'ranges/result.html', context)


def regist_song_form(request):
    ARRENGER_NULL = True
    template = 'ranges/regist_page.html'
    form = SongForm(request.POST or None)
    post = dict()
    # formの更新
    form.fields['lyricists'].choices = [(artist.pk, artist.artist_name)
                                        for artist in Artist.objects.all() if not artist.pk.startswith('V-')]
    form.fields['composers'].choices = [(artist.pk, artist.artist_name)
                                        for artist in Artist.objects.all() if not artist.pk.startswith('V-')]
    form.fields['arrangers'].choices = [(artist.pk, artist.artist_name)
                                        for artist in Artist.objects.all() if not artist.pk.startswith('V-')]
    if form.is_valid():
        title = post['title'] = form.cleaned_data['title']
        lyricist = post['lyricist'] = form.cleaned_data['lyricists']
        composer = post['composer'] = form.cleaned_data['composers']
        arranger = post['arranger'] = form.cleaned_data['arrangers']
        case = False
        if arranger == [''] or arranger == []:
            case = ARRENGER_NULL
        try:
            if case == ARRENGER_NULL:
                Song.objects.get(
                    song_name=title, lyricist__in=lyricist, composer__in=composer)
            else:
                Song.objects.get(
                    song_name=title, lyricist__in=lyricist, composer__in=composer, arranger__in=arranger)
        except Song.DoesNotExist:
            song = Song.objects.create(song_name=title)
            for l in lyricist:
                song.lyricist.add(l)
            for c in composer:
                song.composer.add(c)
            if case is not ARRENGER_NULL:
                for a in arranger:
                    song.arranger.add(a)
            song.save()
            context = {'item': post, 'song_form': SongForm()}
        else:
            context = {'item': post, 'song_form': SongForm(), 'error': True}
        return render(request, template, context)
    return render(request, template, {'song_form': form})


def regist_artist_form(request):
    template = 'ranges/regist_page.html'
    form = ArtistForm(request.POST or None)
    # formの更新
    form.fields['aff'].choices = [(artist.pk, artist.artist_name)
                                  for artist in Artist.objects.all() if not artist.pk.startswith('V-')]
    post = dict()
    if form.is_valid():
        title = post['title'] = form.cleaned_data['name']
        pk = post['PK'] = form.cleaned_data['pk']
        aff = post['Aff'] = form.cleaned_data['aff']
        try:
            Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            artist = Artist.objects.create(artist_id=pk, artist_name=title)
            for a in aff:
                artist.affiliation.add(a)
            artist.save()
            context = {'item': post, 'artist_form': ArtistForm()}
        else:
            context = {'item': post, 'artist_form': ArtistForm(),
                       'error': True}
        return render(request, template, context)
    return render(request, template, {'artist_form': form})


def regist_range_form(request):
    template = 'ranges/regist_page.html'
    form = RangeForm(request.POST or None)
    # form の更新
    form.fields['title'].choices = [
        (song.pk, song.song_name) for song in Song.objects.all()]
    form.fields['artist'].choices = [
        (artist.pk, artist.artist_name) for artist in Artist.objects.all() if not artist.pk.startswith('V-')]
    form.fields['performer'].choices = [
        (artist.pk, artist.artist_name) for artist in Artist.objects.all()]
    form.fields['lowest_note'].choices = form.fields['highest_note'].choices = [
        (note.pk, note.note_name) for note in Note.objects.all()]
    form.fields['fake_note'].choices = [
        ('', '-----')]+[(note.pk, note.note_name) for note in Note.objects.all()]
    form.fields['genre'].choices = [
        (genre.pk, genre.genre_name) for genre in Genre.objects.all()]
    post = dict()
    if form.is_valid():
        title = Song.objects.get(pk=int(form.cleaned_data['title']))
        artist = Artist.objects.get(pk=form.cleaned_data['artist'])
        performer = form.cleaned_data['performer']
        lowest_note = Note.objects.get(pk=form.cleaned_data['lowest_note'])
        highest_note = Note.objects.get(pk=form.cleaned_data['highest_note'])
        fake = form.cleaned_data['fake_note']
        if fake:
            fake_note = Note.objects.get(pk=fake)
        genre = Genre.objects.get(pk=form.cleaned_data['genre'])
        release_date = form.cleaned_data['release_date']
        is_original = True
        if form.cleaned_data['is_original'] == 'False':
            is_original = False
        song_name = title.song_name
        artist_name = artist.artist_name
        post['title'] = song_name + ' / ' + artist_name

        try:
            Range.objects.get(song=title, artist=artist, origin=is_original)
        except Range.DoesNotExist:
            if fake:
                data = Range.objects.create(
                    song=title,
                    artist=artist,
                    lowest_note=lowest_note,
                    highest_note=highest_note,
                    fake_note=fake_note,
                    genre=genre,
                    release_date=release_date
                )
            else:
                data = Range.objects.create(
                    song=title,
                    artist=artist,
                    lowest_note=lowest_note,
                    highest_note=highest_note,
                    genre=genre,
                    release_date=release_date
                )
            for p in performer:
                data.performer.add(p)
            context = {'item': post, 'range_form': RangeForm(), }
        else:
            context = {'item': post, 'range_form': RangeForm(), 'error': True}
        return render(request, template, context)
    return render(request, template, {'range_form': form})
