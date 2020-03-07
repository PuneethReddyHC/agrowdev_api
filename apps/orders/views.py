from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from  orders.models import ShoppingCart, OrderInfo, OrderProducts
from  orders.serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from  utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    Shopping cart function
    list:
        Get Shopping Cart Details
    create:
        add to Shopping Cart
    delete:
        Delete shopping history
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    lookup_field = "products_id"

    # 库存数-1
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        products = shop_cart.products
        products.products_num -= shop_cart.nums
        products.save()

    # 库存数+1
    def perform_destroy(self, instance):
        products = instance.products
        products.products_num += instance.nums
        products.save()
        # 取products在del之前取之后就被删掉了
        instance.delete()

    # 更新库存
    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        # 先保存之前的数据existed_nums
        saved_record = serializer.save()
        # 变化的数量
        nums = saved_record.nums - existed_nums
        products = saved_record.products
        products.products_num -= nums
        products.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    Order management
    list:
        Get personal order
    delete:
        Delete order
    create:
        Add order
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # 获取到用户购物车里的商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_products = OrderProducts()
            order_products.products = shop_cart.products
            order_products.products_num = shop_cart.nums
            order_products.order = order
            order_products.save()

            shop_cart.delete()
        return order


from rest_framework.views import APIView
from  utils.alipay import AliPay
from settings import ali_pub_key_path, private_key_path
from rest_framework.response import Response


class AlipayView(APIView):
    def get(self, request):
        """
        Handle Alipay's return_url return
        """
        processed_dict = {}
        # 1. 获取GET中参数
        for key, value in request.GET.items():
            processed_dict[key] = value
        # 2. 取出sign
        sign = processed_dict.pop("sign", None)

        # 3. 生成ALipay对象
        alipay = AliPay(
            appid="2016091200490210",
            app_notify_url="http://115.159.122.64:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://115.159.122.64:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        # 这里可以不做操作。因为不管发不发return url。notify url都会修改订单状态。
        if verify_re is True:
            order_sn = processed_dict.get('out_orders_no', None)
            orders_no = processed_dict.get('orders_no', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.orders_no = orders_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("/index/#/app/home/member/order")
            # response.set_cookie("nextPath","pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response

    def post(self, request):
        """
        Handling Alipay's notify_url
        """
        # 1. 先将sign剔除掉
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        # 2. 生成一个Alipay对象
        alipay = AliPay(
            appid="2016091200490210",
            app_notify_url="http://115.159.122.64:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://115.159.122.64:8000/alipay/return/"
        )

        # 3. 进行验签，确保这是支付宝给我们的
        verify_re = alipay.verify(processed_dict, sign)

        # 如果验签成功
        if verify_re is True:
            order_sn = processed_dict.get('out_orders_no', None)
            orders_no = processed_dict.get('orders_no', None)
            orders_status = processed_dict.get('orders_status', None)

            # 查询数据库中存在的订单
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 订单商品项
                order_products = existed_order.products.all()
                # 商品销量增加订单中数值
                for order_good in order_products:
                    products = order_good.products
                    products.sold_num += order_good.products_num
                    products.save()

                # 更新订单状态，填充支付宝给的交易凭证号。
                existed_order.pay_status = orders_status
                existed_order.orders_no = orders_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            # 将success返回给支付宝，支付宝就不会一直不停的继续发消息了。
            return Response("success")
