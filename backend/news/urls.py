from django.conf.urls import url
from . import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.news_list, name='news'),
    url(r'^page-(?P<page_number>[0-9]+)/$', views.news_list, name='news'),
]
