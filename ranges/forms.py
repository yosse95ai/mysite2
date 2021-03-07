from django import forms

from .models import Artist, Song, Genre, Note, Range


class SongForm(forms.Form):
    ARTIST_CHOICES = [(artist.pk, artist.artist_name)
                      for artist in Artist.objects.all() if not artist.pk.startswith('V-')]
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(
            attrs={'class': 'input is-small', 'type': 'text', 'placeholder':'曲名を入力'}),
        max_length=100,
        required=True,
    )
    lyricists = forms.MultipleChoiceField(
        label='Lyricists',
        widget=forms.SelectMultiple(attrs={'id': 'lyricists', 'size': 5, }),
        choices=ARTIST_CHOICES,
        required=True,
    )
    composers = forms.MultipleChoiceField(
        label='Composer',
        widget=forms.SelectMultiple(attrs={'id': 'composers', 'size': 5, }),
        choices=ARTIST_CHOICES,
        required=True,
    )
    arrangers = forms.MultipleChoiceField(
        label='Arrangers',
        widget=forms.SelectMultiple(attrs={'id': 'arrangers', 'size': 5, }),
        choices=[('', '-----')]+ARTIST_CHOICES,
        required=False,
    )


class ArtistForm(forms.Form):
    ARTIST_CHOICES = [(artist.pk, artist.artist_name)
                      for artist in Artist.objects.all() if not artist.pk.startswith('V-')]
    name = forms.CharField(
        label='Name',
        max_length=50,
        required=True
    )
    pk = forms.CharField(
        label='PK',
        max_length=10,
        required=True
    )
    aff = forms.MultipleChoiceField(
        label='Aff',
        choices=[('', '-----')]+ARTIST_CHOICES,
        widget=forms.SelectMultiple(attrs={'id': 'aff', 'size': 5, }),
        required=False
    )

    def updateChoice(self):
        self.ARTIST_CHOICES = [(artist.pk, artist.artist_name)
                               for artist in Artist.objects.all() if not artist.pk.startswith('V-')]


class RangeForm(forms.Form):
    SONG_CHOICES = [(song.pk, song.song_name) for song in Song.objects.all()]
    ARTIST_CHOICES = [(artist.pk, artist.artist_name)
                      for artist in Artist.objects.all() if not artist.pk.startswith('V-')]
    PERFORMER_CHOICES = [(artist.pk, artist.artist_name)
                         for artist in Artist.objects.all()]
    NOTE_CHOICES = [(note.pk, note.note_name) for note in Note.objects.all()]
    GENRE_CHOICES = [(genre.pk, genre.genre_name)
                     for genre in Genre.objects.all()]
    title = forms.ChoiceField(
        label='Song',
        choices=SONG_CHOICES,
        required=True,
    )
    artist = forms.ChoiceField(
        label='Artist',
        choices=ARTIST_CHOICES,
        required=True,
    )
    performer = forms.MultipleChoiceField(
        label='Performer',
        widget=forms.SelectMultiple(attrs={'id': 'performer', 'size': 5, }),
        choices=PERFORMER_CHOICES,
        required=True,
    )
    lowest_note = forms.ChoiceField(
        label='Lowest_note',
        choices=NOTE_CHOICES,
        required=True,
    )
    highest_note = forms.ChoiceField(
        label='Highest_note',
        choices=NOTE_CHOICES,
        required=True,
    )
    fake_note = forms.ChoiceField(
        label='Fake_note',
        choices=[('', '-----')]+NOTE_CHOICES,
        required=False,
    )
    genre = forms.ChoiceField(
        label='Genre',
        choices=GENRE_CHOICES,
        required=True,
    )
    release_date = forms.DateTimeField(
        label='release date',
        required=True,
        widget=forms.DateTimeInput(attrs={"type": "date"}),
        input_formats=['%Y-%m-%d'],
    )
    is_original = forms.ChoiceField(
        label='is_original',
        widget=forms.RadioSelect,
        choices=[(True, 'YES'), (False, 'NO')],
        initial=True,
    )
