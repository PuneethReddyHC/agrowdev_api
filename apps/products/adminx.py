# encoding: utf-8
__author__ = 'puneeth'
__date__ = '2020/3/3 0013 20:26'

import xadmin
from .models import Products, ProductsCategory, ProductsImage, ProductsCategoryBrand, Banner, HotSearchWords
from .models import IndexAd


class ProductsAdmin(object):
    list_display = ["name", "click_num", "sold_num", "fav_num", "products_num", "market_price",
                    "shop_price", "products_brief", "products_desc", "is_new", "is_hot", "add_time"]
    search_fields = ['name', ]
    list_editable = ["is_hot", ]
    list_filter = ["name", "click_num", "sold_num", "fav_num", "products_num", "market_price",
                   "shop_price", "is_new", "is_hot", "add_time", "category__name"]

    class ProductsImagesInline(object):
        model = ProductsImage
        exclude = ["add_time"]
        extra = 1
        style = 'tab'

    inlines = [ProductsImagesInline]


class ProductsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


class ProductsBrandAdmin(object):
    list_display = ["category", "image", "name", "desc"]

    def get_context(self):
        context = super(ProductsBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = ProductsCategory.objects.filter(category_type=1)
        return context


class BannerProductsAdmin(object):
    list_display = ["products", "image", "index"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


class IndexAdAdmin(object):
    list_display = ["category", "products"]


xadmin.site.register(Products, ProductsAdmin)
xadmin.site.register(ProductsCategory, ProductsCategoryAdmin)
xadmin.site.register(Banner, BannerProductsAdmin)
xadmin.site.register(ProductsCategoryBrand, ProductsBrandAdmin)

xadmin.site.register(HotSearchWords, HotSearchAdmin)
xadmin.site.register(IndexAd, IndexAdAdmin)

