from datetime import datetime
from django.db import models
# 传统做法，从user.models中引入
from user.models import UserProfile
from products.models import Products
# 但是当第三方模块根本不知道你的user model在哪里如何导入呢
from django.contrib.auth import get_user_model
# 这个方法会去setting中找AUTH_USER_MODEL
User = get_user_model()


# Create your models here.
class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey (User, on_delete = models.CASCADE, verbose_name = u"user")
    products = models.ForeignKey (Products, on_delete = models.CASCADE, verbose_name = u"products")
    nums = models.IntegerField (default = 0, verbose_name = "purchased quantity")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = u"Add time")
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = verbose_name
        unique_together = ("user", "products")

    def __str__(self):
        return "%s(%d)".format(self.products.name, self.nums)


class OrderInfo(models.Model):
    """
    订单信息
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "Success"),
        ("TRADE_CLOSED", "Timeout closed"),
        ("WAIT_BUYER_PAY", "Transaction Creation"),
        ("TRADE_FINISHED", "End of transaction"),
        ("paying", "To be paid"),
    )
    PAY_TYPE = (
        ("alipay", "Alipay"),
        ("wechat", "Wechat"),
    )

    user = models.ForeignKey (User, on_delete = models.CASCADE, verbose_name = "user")
    # unique order number unique
    order_sn = models.CharField (max_length = 30, null = True, blank = True, unique = True, verbose_name = "order number")
    # WeChat payment may be used
    nonce_str = models.CharField (max_length = 50, null = True, blank = True, unique = True, verbose_name = "random encrypted string")
    # Associated with Alipay transaction number and this system
    orders_no = models.CharField (max_length = 100, unique = True, null = True, blank = True, verbose_name = u"Transaction number")
    # Just in case the user paid half of the payment
    pay_status = models.CharField (choices = ORDER_STATUS, default = "paying", max_length = 30, verbose_name = "Order Status")
    # Order payment type
    pay_type = models.CharField (choices = PAY_TYPE, default = "alipay", max_length = 10, verbose_name = "payment type")
    post_script = models.CharField (max_length = 200, verbose_name = "Order message")
    order_mount = models.FloatField (default = 0.0, verbose_name = "Order Amount")
    pay_time = models.DateTimeField (null = True, blank = True, verbose_name = "pay time")
    # User's basic information
    address = models.CharField (max_length = 100, default = "", verbose_name = "Shipping Address")
    signer_name = models.CharField (max_length = 20, default = "", verbose_name = "Signee")
    singer_mobile = models.CharField (max_length = 11, verbose_name = "contact phone")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = "Add Time")
    class Meta:
        verbose_name = u"order information"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderProducts(models.Model):
    """
    Product details in the order
    """
    # One order corresponds to multiple products, so add a foreign key
    order = models.ForeignKey (OrderInfo, on_delete = models.CASCADE, verbose_name = "Order Information", related_name = "products")
    # Two foreign keys form an association table
    products = models.ForeignKey (Products, on_delete = models.CASCADE, verbose_name = "products")
    products_num = models.IntegerField (default = 0, verbose_name = "number of products")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = "Add Time")
    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)