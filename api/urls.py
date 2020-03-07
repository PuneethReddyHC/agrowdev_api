from django.views.static import serve
# from django.contrib import admin

# Django Rest Framework
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views

from rest_framework_jwt.views import obtain_jwt_token
from orders.views import  AlipayView
from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter
from products.views import ProductsListViewSet, CategoryViewset, BannerViewset, IndexCategoryViewset, HotSearchsViewset
from orders.views import ShoppingCartViewset, OrderViewset, AlipayView
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset

from post.apiview import PostBaseInfoListViewset, PostDetailInfoListViewset
from album.apiview import AlbumBaseInfoListViewset, AlbumDetailInfoListViewset
from movie.apiview import MovieBaseInfoListViewset, MovieDetailInfoListViewset
from book.apiview import BookBaseInfoListViewset, BookDetailInfoListViewset, BookNoteBaseInfoListViewset, BookNoteDetailInfoListViewset
from material.apiview import CategoryListViewset, SingleLevelCategoryListViewset, TagListViewset, \
    MaterialBannerListViewset, PostBaseInfoListViewset, PostLikeViewset, VerifyPostAuthViewset
from comment.apiview import CommentDetailListViewset, CommentLikeViewset
from base.apiview import SiteInfoViewset, BloggerInfoViewset, FriendLinkListViewset
from user.apiview import EmailCodeViewset
from post_user_operation.apiview import QiniuTokenViewset
from index.apiview import SearchViewViewSet
from post_apps.utils.CustomRSS import LatestEntriesFeed
from user.views import SmsCodeViewset

router = DefaultRouter()

# 素材相关
router.register(r'categorys', CategoryListViewset, base_name='categorys')
router.register(r'category', SingleLevelCategoryListViewset, base_name='category')
router.register(r'tags', TagListViewset, base_name='tags')
router.register(r'banners', MaterialBannerListViewset, base_name='banners')

# 文章相关
router.register(r'postBaseInfos', PostBaseInfoListViewset, base_name="postBaseInfos")
router.register(r'postDetailInfos', PostDetailInfoListViewset, base_name="postDetailInfos")

# 图集相关
router.register(r'albumBaseInfos', AlbumBaseInfoListViewset, base_name="albumBaseInfos")
router.register(r'albumDetailInfos', AlbumDetailInfoListViewset, base_name="albumDetailInfos")

# 电影
router.register(r'movieBaseInfos', MovieBaseInfoListViewset, base_name="movieBaseInfos")
router.register(r'movieDetailInfos', MovieDetailInfoListViewset, base_name="movieDetailInfos")

# 图书
router.register(r'bookBaseInfos', BookBaseInfoListViewset, base_name='bookBaseInfos')
router.register(r'bookDetailInfos', BookDetailInfoListViewset, base_name='bookDetailInfos')

# 图书笔记
router.register(r'bookNoteBaseInfos', BookNoteBaseInfoListViewset, base_name='bookNoteBaseInfos')
router.register(r'bookNoteDetailInfos', BookNoteDetailInfoListViewset, base_name='bookNoteDetailInfos')

# 时光轴
router.register(r'postBaseInfos', PostBaseInfoListViewset, base_name="postBaseInfos")

# 网站信息
router.register(r'siteInfo', SiteInfoViewset, base_name="siteInfo")
# 博主信息
router.register(r'blogger', BloggerInfoViewset, base_name="blogger")
# 友情链接
router.register(r'friendlinks', FriendLinkListViewset, base_name="friendlinks")
# 评论
router.register(r'comments', CommentDetailListViewset, base_name="comments")
router.register(r'likePost', PostLikeViewset, base_name="likePost")
router.register(r'likeOrUnlikeComment', CommentLikeViewset, base_name="likeOrUnlikeComment")

# 邮箱验证码
router.register(r'emailCode', EmailCodeViewset, base_name="emailCode")
# 验证文章权限
router.register(r'verifyPostAuth', VerifyPostAuthViewset, base_name="verifyPostAuth")
# 七牛云token
router.register(r'qiniuToken', QiniuTokenViewset, base_name='qiniuToken')

# 搜索
router.register("search", SearchViewViewSet, base_name="search")
# 配置products的url,这个basename是干啥的
router.register(r'products', ProductsListViewSet, base_name="products")

# 配置Category的url
router.register(r'categories', CategoryViewset, base_name="categories")

# 配置codes的url
router.register(r'code', SmsCodeViewset, base_name="code")


# 配置用户收藏的url
router.register(r'userfavs', UserFavViewset, base_name="userfavs")

# 配置用户留言的url
router.register(r'messages', LeavingMessageViewset, base_name="messages")

# 收货地址
router.register(r'address', AddressViewset, base_name="address")

# 购物车
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")

# 订单相关url
router.register(r'orders', OrderViewset, base_name="orders")

# 首页banner轮播图url
router.register(r'banners', BannerViewset, base_name="banners")

# 首页系列商品展示url
router.register(r'indexproducts', IndexCategoryViewset, base_name="indexproducts")

urlpatterns = [
    path('', include(router.urls)),
    

    # RSS订阅
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   
    path('docs/', include_docs_urls(title="docs", public=False)),

    # jwt的token认证
    path('login/', obtain_jwt_token),

    # 支付宝支付相关接口
    path('alipay/return/', AlipayView.as_view()),
    
    path('', include('social_django.urls', namespace='social')),
]