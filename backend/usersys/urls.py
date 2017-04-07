from django.conf.urls import url

from . import views

app_name = 'usersys'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^registration/$', views.registration, name='registration'),
]
