import datetime

from django.db import models
from django.utils import timezone


class Artist(models.Model):
    artist_id = models.CharField(max_length=10, primary_key=True)
    artist_name = models.CharField("Artist's name", max_length=50)

    def __str__(self):
        return self.artist_name

    class Meta:
        ordering = ('artist_name', )


class Song(models.Model):
    class Meta:
        ordering = ('song_name',)
        
    song_id = models.AutoField(primary_key=True)
    song_name = models.CharField("Tilte", max_length=100)
    composer = models.ManyToManyField(Artist, related_name="composer_name")
    lyricist = models.ManyToManyField(Artist, related_name="lyricist_name")
    arranger = models.ManyToManyField(
        Artist, related_name="arranger_name", null=True, blank=True)

    def __str__(self):
        return self.song_name+': '+",".join([a.artist_name for a in self.composer.all()])

    def get_composer(self):
        return "\n".join([a.artist_name for a in self.composer.all()])

    def get_lyricist(self):
        return "\n".join([a.artist_name for a in self.lyricist.all()])

    def get_arranger(self):
        return "\n".join([a.artist_name for a in self.arranger.all()])

    get_composer.short_description = 'Composer'
    get_lyricist.short_description = 'Lyricist'
    get_arranger.short_description = 'Arranger'



class Note(models.Model):
    note_id = models.CharField(max_length=5, primary_key=True)
    note_name = models.CharField(max_length=50)

    def __str__(self):
        return self.note_name


class Genre(models.Model):
    genre_id = models.CharField(max_length=5, primary_key=True)
    genre_name = models.CharField(max_length=50)

    def __str__(self):
        return self.genre_name


class Range(models.Model):
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE, to_field="song_id", related_name="song")
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, to_field="artist_id", related_name="artist")
    performer = models.ManyToManyField(Artist, related_name="performer_name")
    lowest_note = models.ForeignKey(
        Note, on_delete=models.CASCADE, to_field="note_id", related_name="low_note")
    highest_note = models.ForeignKey(
        Note, on_delete=models.CASCADE, to_field="note_id", related_name="high_note")
    fake_note = models.ForeignKey(
        Note, on_delete=models.CASCADE, to_field="note_id", related_name="fake_note", null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    release_date = models.DateTimeField('date released', null=True, blank=True)
    pub_date = models.DateTimeField(default=timezone.now())
    latest_update = models.DateTimeField('date update lately', auto_now=True)

    def __str__(self):
        s_name = Song.objects.get(pk=self.song_id)
        a_name=Artist.objects.get(pk=self.artist_id)
        return s_name.song_name+'/'+a_name.artist_name

    class Meta:
        unique_together = ['song', 'artist']
