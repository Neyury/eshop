from django.db import models
import PIL
import re


verbose_name = "Статьи"


def path_image(instance, filename):
    if instance.id:
        instance_name = re.sub('[^a-zа-яе0-9 ]', '', instance.title.lower().strip()).replace(' ', '_')
        file_name = '{0}.{1}'.format(instance_name, filename.split('.')[-1])

        return 'article_images/{0}/main_image/{1}'.format(instance.id, file_name[:20])
    else:
        return 'article_images/main_images/{0}'.format(filename)


class Article(models.Model):
    image = models.ImageField('Изображение', upload_to=path_image, null=True, blank=True)
    title = models.TextField('Название')
    content = models.TextField('Контент',  blank=True)
    pub_date = models.DateField('Дата публикации', auto_now_add=True)
    views = models.IntegerField('Просмотры', default=0)
    hidden = models.BooleanField('Скрыть в выдаче', default=False)


    def get_short_content(self):

        if len(self.content) < 500:
            return self.content
        else:
            return self.content[:500] + '...'

    def get_short_title(self):
        if len(self.title) < 75:
            return self.title
        else:
            return self.title[:75] + '...'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-pub_date']


