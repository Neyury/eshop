from django.conf.urls import url
from . import views

app_name = 'articles'
urlpatterns = [
    url(r'^$', views.articles_list, name='articles'),
    url(r'^page-(?P<page_number>[0-9]+)/$', views.articles_list, name='articles'),
    url(r'^(?P<article_id>[0-9]+)/$', views.article, name='article'),
]
