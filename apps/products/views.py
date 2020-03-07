from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import TokenAuthentication

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from  products.filters import ProductsFilter
from  products.serializers import ProductsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer, \
    HotWordsSerializer
from .models import Products, ProductsCategory, Banner, HotSearchWords
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.cache.mixins import CacheResponseMixin
# 设置登录与未登录限速
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# 商品列表分页类
class ProductsPagination(PageNumberPagination):
    page_size = 12
    # 向后台要多少条

    page_size_query_param = 'page_size'
    # 定制多少页的参数
    page_query_param = "page"
    max_page_size = 100


# class ProductsListView(mixins.ListModelMixin, generics.GenericAPIView):
# class ProductsListView(ListAPIView):
# class ProductsListView(mixins.ListModelMixin, viewsets.GenericViewSet):
class ProductsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Product list page, pagination, search, filter, sort, get details of a specific product
    """

    # queryset是一个属性
    # good_viewset.queryset就可以访问到
    # 函数就必须调用good_viewset.get_queryset()函数
    # 如果有了下面的get_queryset。那么上面的这个就不需要了。
    # queryset = Products.objects.all()

    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = ProductsSerializer
    pagination_class = ProductsPagination
    queryset = Products.objects.all()

    # 设置列表页的单独auth认证也就是不认证
    # authentication_classes = (TokenAuthentication,)

    # 设置三大常用过滤器之DjangoFilterBackend, SearchFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 设置排序
    ordering_fields = ('sold_num', 'shop_price')
    # 设置filter的类为我们自定义的类
    filter_class = ProductsFilter

    # 设置我们的search字段
    search_fields = ('name', 'products_brief', 'products_desc')

    # 设置我们需要进行过滤的字段
    # filter_fields = ('name', 'shop_price')



    # def get_queryset(self):
    #     # 价格大于100的
    #     price_min = self.request.query_params.get('price_min', 0)
    #     if price_min:
    #         self.queryset = Products.objects.filter(shop_price__gt=int(price_min)).order_by('-add_time')
    #     return self.queryset
# class ProductsListView(APIView):
#     """
#     列出所有商品
#     """
#     def get(self, request, format=None):
#         products = Products.objects.all()[:10]
#         # 因为前面的是一个列表，加many=True
#         products_json = ProductsSerializer(products, many=True)
#         return Response(products_json.data)

    # def post(self, request, format=None):
    #     serializer = ProductsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 商品点击数+1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        Product category list data
    retrieve:
        Get product category details
    """
    queryset = ProductsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Get Carousel List
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Home Product Classification Data
    """
    queryset = ProductsCategory.objects.filter(is_tab=True, name__in=["Fresh food "," drinks"])
    serializer_class = IndexCategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Get Hot Search Word List
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer
