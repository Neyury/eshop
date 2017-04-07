from django.contrib import admin
from .models import Brand, BrandColor, Product, ProductCategory, ProductColor,  BrandSize, ProductImage, ProductSize


class BrandColorAdmin(admin.TabularInline):
    model = BrandColor
    extra = 1


class BrandSizeAdmin(admin.TabularInline):
    model = BrandSize
    extra = 1


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [
        BrandColorAdmin,
        BrandSizeAdmin,
    ]


class ProductColorAdmin(admin.TabularInline):
    model = ProductColor
    extra = 1


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSizeAdmin(admin.TabularInline):
    model = ProductSize
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name', 'category', 'brand', 'description')
    list_display = ('id', 'name', 'brand', 'category','views', 'images')
    list_display_links = ('id', 'name')
    readonly_fields = ('views',)
    list_filter = [
        'category',
        ('brand', admin.RelatedOnlyFieldListFilter),
        'den',
        'discount',
        'hidden',
        'created_automatically',
    ]

    fields = (
        ('name','views' ),
        'brand',
        'category',
        'den',
        'amount',
        #('price', 'discount_price'),
        'composition',
        'description',
        'discount',
        'hidden',
    )
    inlines = [
        ProductSizeAdmin,
        ProductColorAdmin,
        ProductImageAdmin
    ]

    def images(self, obj):
        images =  len(ProductImage.objects.filter(product=obj.id))

        if images:
            return images
        return None


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','parent', 'order')
    list_editable = ('parent', 'order' )
    search_fields = ['name']

    list_filter = [
        ('parent', admin.RelatedOnlyFieldListFilter),
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)