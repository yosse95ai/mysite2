from django.contrib import admin
from ranges.models import Note,Artist,Song,Genre,Range

admin.site.register(Note)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Range)