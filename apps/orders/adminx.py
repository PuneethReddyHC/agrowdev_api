# encoding: utf-8
__author__ = 'puneeth'
__date__ = '2020/3/3 0013 20:27'

import xadmin
from .models import ShoppingCart, OrderInfo, OrderProducts


class ShoppingCartAdmin(object):
    list_display = ["user", "products", "nums", ]


class OrderInfoAdmin(object):
    list_display = ["user", "order_sn",  "orders_no", "pay_status", "post_script", "order_mount",
                    "order_mount", "pay_time", "add_time"]

    class OrderProductsInline(object):
        model = OrderProducts
        exclude = ['add_time', ]
        extra = 1
        style = 'tab'

    inlines = [OrderProductsInline, ]


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
