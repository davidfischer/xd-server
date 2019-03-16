from django.contrib import admin

from .models import Publication, Crossword, Clue


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class CrosswordAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'author', 'editor', 'date')
    list_filter = ('publication__name',)
    search_fields = ('author', 'editor')


class ClueAdmin(admin.ModelAdmin):
    list_display = ('clue', 'answer', 'crossword', 'pos')
    list_select_related = ('crossword',)


admin.site.register(Publication, PublicationAdmin)
admin.site.register(Crossword, CrosswordAdmin)
admin.site.register(Clue, ClueAdmin)
