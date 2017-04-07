from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404
from .models import  News
from django.utils import timezone
from catalog.models import ProductCategory

elements_on_the_page = 10


def news_list(request, page_number=1):
    context = dict()

    news_list =  News.objects.filter(pub_date__lte=timezone.now(), hidden_date__gt=timezone.now())

    current_page = Paginator(news_list, elements_on_the_page)

    if int(page_number) not in range(1, current_page.num_pages+1):
        raise Http404('Страница не найдена')

    context['news_list'] = current_page.page(page_number)
    context['category_list'] = ProductCategory.objects.all()

    return render(request, 'news/news.html', context)


