from datetime import datetime
from django.db import models
from  products.models import Products
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏操作
    """
    user = models.ForeignKey (User, on_delete = models.CASCADE, verbose_name = "user")
    products = models.ForeignKey (Products, on_delete = models.CASCADE, verbose_name = "products", help_text = "products id")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = u"Add time")
    class Meta:
        verbose_name = 'User Favorites'
        verbose_name_plural = verbose_name

        # 多个字段作为一个联合唯一索引
        unique_together = ("user", "products")

    def __str__(self):
        return self.user.username


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey (User, on_delete = models.CASCADE, verbose_name = "user")
    province = models.CharField (max_length = 100, default = "", verbose_name = "province")
    city = models.CharField (max_length = 100, default = "", verbose_name = "city")
    district = models.CharField (max_length = 100, default = "", verbose_name = "region")
    address = models.CharField (max_length = 100, default = "", verbose_name = "detailed address")
    signer_name = models.CharField (max_length = 100, default = "", verbose_name = "Signee")
    signer_mobile = models.CharField (max_length = 11, default = "", verbose_name = "phone")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = "Add Time")
    class Meta:
        verbose_name = "Shipping address"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "Message"),
        (2, "Complaint"),
        (3, "Ask"),
        (4, "after sales"),
        (5, "Buy")
    )
    user = models.ForeignKey (User, on_delete = models.CASCADE, verbose_name = "user")
    message_type = models.IntegerField (default = 1, choices = MESSAGE_CHOICES, verbose_name = "message type",help_text = u"Message type: 1 (message), 2 (complaint), 3 (inquiry), 4 (after-sale), 5 (purchase)")
    subject = models.CharField (max_length = 100, default = "", verbose_name = "topic")
    message = models.TextField (default = "", verbose_name = "message content", help_text = "message content")
    file = models.FileField (upload_to = "message/images/", verbose_name = "uploaded file", help_text = "uploaded file")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = "Add Time")
    class Meta:
        verbose_name = "User Comments"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject