from django.contrib import admin
from ranges.models import Note,Artist,Song,Genre,Range

class RangeAdmin(admin.ModelAdmin):
    list_display = ('song', 'artist', 'pub_date')
    filter_horizontal = ('performer',)

class SongAdmin(admin.ModelAdmin):
    filter_horizontal = ('composer','lyricist','arranger')
    list_display = ('song_name',)


admin.site.register(Note)
admin.site.register(Artist)
admin.site.register(Song,SongAdmin)
admin.site.register(Genre)
admin.site.register(Range,RangeAdmin)
