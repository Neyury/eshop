from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Article
from django.http import Http404
from catalog.models import ProductCategory

elements_on_the_page = 10

def articles_list(request, page_number=1):
    context = dict()

    article_list = Article.objects.filter(hidden=False)
    current_page = Paginator(article_list, elements_on_the_page)

    if int(page_number) not in range(1, current_page.num_pages+1):
        raise Http404('Страница не найдена')

    context['article_list'] = current_page.page(page_number)
    context['category_list'] = ProductCategory.objects.all()

    return render(request, 'articles/articles.html', context)


def article(request, article_id):
    context = dict()

    article = get_object_or_404(Article, pk=article_id, hidden=False)

    if  article:
        article.views += 1
        article.save()

    context['category_list'] = ProductCategory.objects.all()
    context['article'] = article

    return render(request, 'articles/article.html', context)
