# encoding: utf-8
from django.db.models import Q

__author__ = 'puneeth'
__date__ = '2018/2/14 0014 16:44'

from  products.models import Products, ProductsCategory, ProductsImage, Banner, ProductsCategoryBrand, IndexAd, HotSearchWords
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsCategory
        fields = "__all__"


class ProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImage
        fields = ("image",)

class ProductsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductsImageSerializer(many=True)

    class Meta:
        model = Products
        # fields = ('category', 'products_sn', 'name', 'click_num', 'sold_num', 'market_price')
        fields = "__all__"


class CategorySerializer3(serializers.ModelSerializer):
    """
    商品三级类别序列化
    """
    class Meta:
        model = ProductsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品二级类别序列化
    """
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = ProductsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品一级类别序列化
    """
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = ProductsCategory
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    # 首页系列商标一对多
    brands = BrandSerializer(many=True)
    # 首页商品自定义methodfield获取相关类匹配
    products = serializers.SerializerMethodField()
    # 获取二级类
    sub_cat = CategorySerializer2(many=True)
    # 获取广告商品(一个的)
    ad_products = serializers.SerializerMethodField()

    def get_ad_products(self, obj):
        products_json = {}
        ad_products = IndexAd.objects.filter(category_id=obj.id, )
        if ad_products:
            good_ins = ad_products[0].products
            products_json = ProductsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return products_json

    def get_products(self, obj):
        all_products = products.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        products_serializer = ProductsSerializer(all_products, many=True, context={'request': self.context['request']})
        return products_serializer.data

    class Meta:
        model = ProductsCategory
        fields = "__all__"


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"
