from django.db import models
from django.db.models import F
from django.core.validators import RegexValidator
import re
import PIL
from PIL import Image
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust,ResizeToFill

verbose_name = "Каталог"

class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(ColorField, self).__init__(*args, **kwargs)


def path_image(instance, filename):
    if instance.product:
        instance_product_name = re.sub('[^a-zа-яе0-9 ]', '', instance.product.name.lower().strip()).replace(' ', '_')
        file_name = '{0}.{1}'.format(instance_product_name, filename.split('.')[-1])

        return 'product_images/{0}/{1}'.format(instance.product.id, file_name)
    else:
        return 'product_images/{0}'.format(filename)


class Brand(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name', ]


class BrandColor(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField('Название цвета', help_text='Не обязательно', max_length=40, blank=True)
    color = ColorField('Цвет', help_text='rgb в формате HEX', max_length=6, validators=[RegexValidator(regex=r'^[0-9a-fA-F]{6}$')])

    def __str__(self):
        return "{0} ({1})".format(self.color, self.name)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета бренда'


class BrandSize(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.CharField('Стандартное обозначение размера', help_text='S, M, L, 1, 2, 3 и т.д', max_length=7)
    num_size = models.CharField('Числовой размер', help_text='46-48, 50-52 и т.д', max_length=10)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'Размер бренда'
        verbose_name_plural = 'Размеры брендов'


class ProductCategory(models.Model):
    parent = models.ForeignKey('ProductCategory', verbose_name='Родительская категория', null=True, blank=True)
    name = models.CharField(verbose_name='Название',max_length=40)
    order = models.PositiveIntegerField(verbose_name='Очередность', default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['order' ]


class Product(models.Model):
    name = models.CharField('Название', max_length=50)
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ProductCategory, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    den = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField('Количество в упаковке',blank=True, null=True)
    composition = models.CharField('Состав', max_length=200, null=True, blank=True)
    description = models.TextField('Описание', max_length=700, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    available = models.BooleanField('Наличие', default=True)
    discount = models.BooleanField('Акция', default=False)
    hidden = models.BooleanField('Скрыто в выдаче', default=False)
    views = models.PositiveIntegerField('Просмотры', default=0)
    created_automatically = models.BooleanField('Создано программой', default=False, blank=True)


    def get_absolute_url(self):
        return "/catalog/{0}/{1}/".format(self.category.id, self.id)

    def image(self):
        item = ProductImage.objects.filter(product=self.id).first()

        if item:
            return item
        else:
            return None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', ]


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField('Название', help_text='Не обязательно', max_length=40, blank=True)
    color = ColorField('Цвет', help_text='формат HEX', max_length=6, validators=[RegexValidator(regex=r'^[0-9a-fA-F]{6}$')])

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'цвет продукта'
        verbose_name_plural = 'цвета продукта'


class ProductSize(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=12)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'размер продукта'
        verbose_name_plural = 'размеры продукта'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=40, blank=True)
    image = models.ImageField('Изображение', upload_to=path_image)
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFit(278, 400)], format='JPEG', options={'quality': 100})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'изображение продукта'
        verbose_name_plural = 'изображения продукта'


