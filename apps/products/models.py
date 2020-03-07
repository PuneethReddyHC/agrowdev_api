from datetime import datetime
from django.db import models


# Create your models here.


class ProductsCategory(models.Model):
    """
    商品多级分类
    """
    CATEGORY_TYPE = (
        (1, "First Class"),
        (2, "Secodary"),
        (3, "teritary"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="Cartgory Name", help_text="Category Name")
    code = models.CharField(default="", max_length=30, verbose_name="Cartgory code", help_text="Category code")
    desc = models.TextField(default="", verbose_name="Category Desc", help_text="Description")
    # 设置目录树的级别
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="Category Type", help_text="Category Type")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Parent Category", help_text="parent Category",
                                        related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="is tab", help_text="is tab")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="Time")

    class Meta:
        verbose_name = "Add Product"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProductsCategoryBrand(models.Model):
    """
    
    """
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE, related_name='brands', null=True, blank=True, verbose_name="商品类目")
    name = models.CharField(default="", max_length=30, verbose_name="品牌名", help_text="品牌名")
    desc = models.TextField(default="", max_length=200, verbose_name="品牌描述", help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "Add Category"
        verbose_name_plural = verbose_name
        db_table = "products_productsbrand"

    def __str__(self):
        return self.name


class Products(models.Model):
    """
    商品
    """
    category = models.ForeignKey (ProductsCategory, on_delete = models.CASCADE, verbose_name = "Product Category")
    products_sn = models.CharField (max_length = 50, default = "", verbose_name = "product unique post number")
    name = models.CharField (max_length = 100, verbose_name = "Product Name")
    click_num = models.IntegerField (default = 0, verbose_name = "clicks")
    sold_num = models.IntegerField (default = 0, verbose_name = "Product Sales")
    fav_num = models.IntegerField (default = 0, verbose_name = "number of favorites")
    products_num = models.IntegerField (default = 0, verbose_name = "stock count")
    market_price = models.FloatField (default = 0, verbose_name = "market price")
    shop_price = models.FloatField (default = 0, verbose_name = "our shop price")
    products_brief = models.TextField (max_length = 500, verbose_name = "item short description")
    products_desc = models.TextField (max_length = 500, verbose_name = "Product Description")
    # Product cover image displayed in the homepage
    products_front_image = models.ImageField (upload_to = "products/images/", null = True, blank = True, verbose_name = "cover image")
    # Homepage New Products
    is_new = models.BooleanField (default = False, verbose_name = "is new product")
    # Hot products on the product details page, set your own
    is_hot = models.BooleanField (default = False, verbose_name = "is it hot")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = "Add Time")
    class Meta:
        verbose_name = 'Product information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProductsImage(models.Model):
    """
    商品轮播图
    """
    products = models.ForeignKey (Products, on_delete = models.CASCADE, verbose_name = "products", related_name = "images")
    image = models.ImageField (upload_to = "", verbose_name = "picture", null = True, blank = True)
    add_time = models.DateTimeField (default = datetime.now, verbose_name = "Add Time")
    class Meta:
        verbose_name = 'Commodity Carousel'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.products.name


class Banner(models.Model):
    """
    Home carousel product map, adapted to the home page
    """
    products = models.ForeignKey (Products, on_delete = models.CASCADE, verbose_name = "products")
    image = models.ImageField (upload_to = 'banner', verbose_name = "carousel image")
    index = models.IntegerField (default = 0, verbose_name = "carousel order")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = "Add Time")
    class Meta:
        verbose_name = 'Home Carousel'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.products.name


class IndexAd(models.Model):
    """
    首页类别标签右边展示的七个商品广告
    """
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE, related_name='category',verbose_name="商品类目")
    products =models.ForeignKey(Products, on_delete=models.CASCADE, related_name='products')

    class Meta:
        verbose_name = 'Home ad'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.products.name


class HotSearchWords(models.Model):
    """
    搜索栏下方热搜词
    """
    keywords = models.CharField (default = "", max_length = 20, verbose_name = "Hot search term")
    index = models.IntegerField (default = 0, verbose_name = "sort")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = "Add Time")
    class Meta:
        verbose_name = 'Hot search ranking'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords