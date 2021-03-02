from django.contrib import admin
from ranges.models import Note, Artist, Song, Genre, Range


class RangeAdmin(admin.ModelAdmin):
    list_display = ('song', 'artist', 'pub_date')
    filter_horizontal = ('performer',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "song":
            kwargs["queryset"] = Song.objects.all().order_by('song_name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SongAdmin(admin.ModelAdmin):
    filter_horizontal = ('composer', 'lyricist', 'arranger')
    list_display = ('song_name', 'get_composer',
                    'get_lyricist', 'get_arranger',)


admin.site.register(Note)
admin.site.register(Artist)
admin.site.register(Song, SongAdmin)
admin.site.register(Genre)
admin.site.register(Range, RangeAdmin)
