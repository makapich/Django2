from django.contrib import admin

from .models import Author, Quote


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'truncated_bio', 'date_of_birth')
    search_fields = ('name', )

    @staticmethod
    def truncated_bio(obj):
        return (obj.bio[:50] + '...') if len(obj.bio) > 50 else obj.bio


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('truncated_text', 'author')
    search_fields = ('author__name', )

    @staticmethod
    def truncated_text(obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text
