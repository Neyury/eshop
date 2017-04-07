from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title', 'pub_date', 'hidden_date')
    list_editable = ('pub_date', 'hidden_date')
    fields = (
        'title',
        'content',
        'pub_date',
        'hidden_date',
    )


admin.site.register(News, NewsAdmin)