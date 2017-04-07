from django.conf.urls import url
from . import views

app_name = 'catalog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^information/$', views.information, name='information'),
    url(r'^catalog/$', views.catalog, name='catalog'),
    url(r'^catalog/page-(?P<page_number>[0-9]+)/$', views.catalog, name='catalog'),
    url(r'^catalog/search/$', views.search, name='search'),
    url(r'^catalog/search/page-(?P<page_number>[0-9]+)/$', views.search, name='search'),
    url(r'^catalog/(?P<product_category_id>[0-9]+)/$', views.category, name='category'),
    url(r'^catalog/(?P<product_category_id>[0-9]+)/page-(?P<page_number>[0-9]+)/$', views.category, name='category'),
    url(r'^catalog/(?P<product_category_id>[0-9]+)/(?P<product_id>[0-9]+)/$', views.product, name='product'),

]
