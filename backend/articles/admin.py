from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'image',
        'title',
        'content',
        'hidden',
    )


admin.site.register(Article, ArticleAdmin)