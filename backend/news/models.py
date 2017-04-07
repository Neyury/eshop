from django.db import models
import PIL
from django.utils import timezone
verbose_name = "Новости"


class News(models.Model):
    title = models.TextField('Название')
    content = models.TextField('Контент',  blank=True)
    pub_date = models.DateTimeField('Начало показа', default=timezone.now())
    hidden_date = models.DateTimeField('Конец показа', default=timezone.datetime(3000,1,1,0,0))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-pub_date']

