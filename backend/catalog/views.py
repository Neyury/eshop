from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.http import Http404
from .models import Product, Brand, BrandColor, BrandSize, ProductCategory, ProductColor, ProductImage, ProductSize
from news.models import News
from django.utils import timezone
from django.db.models import Count


elements_on_the_page = 30


def get_default_context():
    context = dict()
    category_list = ProductCategory.objects.all()

    context['category_list'] = category_list

    return context


def get_children_categories(id, category_list, buff=list()):
    children = list()
    children.append(id)
    for category in category_list:
        if  category.parent:
            if  category.parent.id == int(id):
                if category.id not in buff:
                    children.append(category.id)
                    children += get_children_categories(category.id, category_list, children)

    return children

def get_parents_category(obj, buff=list()):
    parents = list()
    if  obj.parent:
        if obj not in buff:
            parents.append(obj.parent)
            parents += get_parents_category(obj.parent, parents)

    buff = list()
    for i in range(0, len(parents)):
        buff.append(parents.pop())

    return buff


def information(request):
    context = get_default_context()

    return render(request, 'catalog/info.html', context)


def search(request, page_number=1):
    context = get_default_context()

    product_list = Product.objects.filter(hidden=False)

    if request.GET['find']:
        search_request = request.GET['find'].split()
        for i in range(0, len(search_request)):
            product_list = product_list.filter(name__icontains=search_request[i])


    current_page = Paginator(product_list, elements_on_the_page)

    if int(page_number) not in range(1, current_page.num_pages+1):
        raise Http404('Страница не найдена')

    if request.GET.urlencode():
        context['url_parameters'] = '?' + request.GET.urlencode()

    context['product_list'] = current_page.page(page_number)

    return render(request, 'catalog/search.html', context)


def index(request):
    context = get_default_context()

    product_list = Product.objects.filter(hidden=False)

    max_views = product_list.order_by('views').last().views
    avr_views = max_views / 2

    brand_list = Brand.objects.filter(pk__in=Product.objects.all().values('brand')).annotate(Count('product'))

    context['discount_list'] = product_list.filter(hidden=False, discount=True)[:3]
    context['popular_list'] = product_list.filter(views__gte=avr_views)[:3]
    context['newpub_list'] = product_list.order_by('-date_added')[:3]
    context['brand_list'] = brand_list
    context['news_list'] = News.objects.filter(pub_date__lte=timezone.now(), hidden_date__gt=timezone.now())[:3]
    context['sort'] = request.GET.get('sort')
    return render(request, 'catalog/index.html', context)


def catalog(request, page_number=1):
    context = get_default_context()

    product_list = Product.objects.filter(hidden=False)

    sort = request.GET.get('sort')

    selected_brands = request.GET.getlist('brand')
    selected_dens = request.GET.getlist('den')

    if request.GET.urlencode():
        context['url_parameters'] = '?' + request.GET.urlencode()

    if selected_brands:
        product_list = product_list.filter(brand__in=selected_brands)

    if selected_dens:
        product_list = product_list.filter(den__in=selected_dens)

    if sort == 'discount':
        product_list = product_list.filter(discount=True)

    if sort == 'popular':
        max_views = Product.objects.filter(hidden=False).order_by('views').last().views
        avr_views = max_views/2
        product_list = product_list.filter(views__gte=avr_views)

    if sort == 'newpub':
        product_list = product_list.order_by('-date_added')


    current_page = Paginator(product_list, elements_on_the_page)

    if int(page_number) not in range(1, current_page.num_pages+1):
        raise Http404('Страница не найдена')

    brand_list = Brand.objects.filter(pk__in=Product.objects.all().values('brand')).annotate(Count('product'))
    den_list = Product.objects.filter(hidden=False).exclude(den=None).values('den').annotate(product__count=Count('den')).order_by('den')

    context['product_list'] = current_page.page(page_number)
    context['brand_list'] = brand_list
    context['den_list'] = den_list
    context['sort'] = sort
    context['selected_brands'] = list(map(int, selected_brands))
    context['selected_dens'] = list(map(int, selected_dens))

    return render(request, 'catalog/catalog.html', context)


def category(request, product_category_id, page_number=1):
    context = get_default_context()

    children_categories = get_children_categories(product_category_id, context['category_list'])

    product_list = Product.objects.filter(category__in=children_categories, hidden=False)

    sort = request.GET.get('sort')

    selected_brands = request.GET.getlist('brand')
    selected_dens = request.GET.getlist('den')

    if request.GET.urlencode():
        context['url_parameters'] = '?' + request.GET.urlencode()

    if selected_brands:
        product_list = product_list.filter(brand__in=selected_brands)

    if selected_dens:
        product_list = product_list.filter(den__in=selected_dens)

    if sort == 'discount':
        product_list = product_list.filter(discount=True)

    if sort == 'popular':
        max_views = Product.objects.filter(hidden=False).order_by('views').last().views
        avr_views = max_views
        product_list = product_list.filter(views__gte=avr_views)

    if sort == 'newpub':
        product_list = product_list.order_by('-date_added')

    current_page = Paginator(product_list, elements_on_the_page)

    if int(page_number) not in range(1, current_page.num_pages+1):
        raise Http404('Страница не найдена')

    brand_list = Brand.objects.filter(pk__in=Product.objects.filter(category__in=children_categories).values('brand')).annotate(Count('product'))
    den_list =  Product.objects.filter(category__in= children_categories,hidden=False).exclude(den=None).values('den').annotate(product__count=Count('den')).order_by('den')

    context['product_list'] = current_page.page(page_number)
    context['brand_list'] = brand_list
    context['den_list'] = den_list
    context['category'] = get_object_or_404(ProductCategory, pk=product_category_id)
    context['sort'] = sort
    context['categories'] = get_parents_category(ProductCategory.objects.get(id=product_category_id))
    context['selected_brands'] = list(map(int, selected_brands))
    context['selected_dens'] = list(map(int, selected_dens))

    return render(request, 'catalog/category.html', context)


def product(request,product_category_id, product_id):
    context = get_default_context()

    if request.user.is_staff:
        product = get_object_or_404(Product, pk=product_id, category=product_category_id)
    else:
        product = get_object_or_404(Product, pk=product_id, category=product_category_id, hidden=False)

    if  product:
        product.views += 1
        product.save()

    max_views = Product.objects.filter(hidden=False, brand=product.brand).order_by('views').last().views
    avr_views = max_views/2

    context['product_list'] = Product.objects.filter(hidden=False, brand=product.brand, views__gte=avr_views).exclude(pk=product.id).order_by('views')[:4]
    context['product'] = product
    context['category'] = get_object_or_404(ProductCategory, pk=product_category_id)
    context['categories'] = get_parents_category(ProductCategory.objects.get(id=product_category_id))
    context['size_list'] = ProductSize.objects.filter(product=product_id)
    context['image_list'] = ProductImage.objects.filter(product=product_id)
    context['color_list'] = ProductColor.objects.filter(product=product_id)
    context['brand_color_list'] = BrandColor.objects.filter(brand=product.brand)
    context['brand_size_list'] = BrandSize.objects.order_by('id').filter(brand=product.brand)

    return render(request, 'catalog/product.html', context)


