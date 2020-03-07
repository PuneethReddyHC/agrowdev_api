import uuid
from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import datetime


class UserProfile (AbstractUser):
    """
    user
    """
    nick_name = models.CharField(max_length = 50, default = "", verbose_name = "nickname", help_text = "nickname")
    name = models.CharField(max_length = 30, null = True, blank = True, verbose_name = "Name", help_text = "Name")
    birthday = models.DateTimeField(null = True, blank = True, verbose_name = "birthday", help_text = "birthday")
    gender = models.CharField(max_length = 6, choices = (("male", "Male"), ("female", "Female")), default = "female",
                              verbose_name = "Gender", help_text = "Gender")
    mobile = models.CharField(max_length = 11, null = True, blank = True, verbose_name = "phone", help_text = "phone")
    email = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "mail", help_text = "mail")
    avatar = models.ImageField(upload_to = "user/avatar/image/%Y/%m", null = True, blank = True, verbose_name = "avatar",
                               help_text = "avatar")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def __str__ (self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = verbose_name


class GuestProfile(models.Model):
    """
    The guests
    """
    uuid = models.UUIDField(primary_key = False, default = uuid.uuid4, null = True, blank = True, editable = False)
    username = models.CharField(max_length = 50, null = True, blank = True, verbose_name = "user name", help_text = "user name")
    nick_name = models.CharField(max_length = 50, default = "", verbose_name = "nickname", help_text = "nickname")
    mobile = models.CharField(max_length = 11, null = True, blank = True, verbose_name = "phone", help_text = "phone")
    email = models.CharField(max_length = 100, null = True, blank = True, verbose_name = "mail", help_text = "mail")
    avatar = models.ImageField(upload_to = "user/avatar/image/%Y/%m", default = 'user/avatar/image/guest.png', null = True,
                               blank = True, verbose_name = "Avatar", help_text = "Avatar")
    is_subcribe = models.BooleanField(default = True, blank = True, verbose_name = "whether to subscribe to notification emails", help_text = "notification emails other than verification code notification emails")
    add_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "Add Time", help_text = "Add Time")

    def __str__ (self):
        return self.nick_name

    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):
    """
    E-mail verification code
    """
    CODE_TYPE = (
        ("register", "register"),
        ("forget", "Retrieve Password"),
        ("update_email", "Modify Email"),
        ("comment", "comment")
    )

    code = models.CharField(max_length = 20, verbose_name = "Verification Code", help_text = "Verification Code")
    email = models.EmailField(max_length = 50, verbose_name = "mailbox", help_text = "mailbox")
    send_type = models.CharField(max_length = 15, choices = CODE_TYPE, verbose_name = "Verification code type", help_text = "Verification code type")
    send_time = models.DateTimeField(auto_now_add = True, null = True, blank = True, verbose_name = "send time", help_text = "send time")

    def __str__ (self):
        return '{0}[{1}]'. format (self.code, self.email)

    class Meta:
        verbose_name = "Mail Verification Code"
        verbose_name_plural = verbose_name

class VerifyCode(models.Model):
    """
    SMS verification code, backfill verification code for verification. Can be saved in redis
    """
    code = models.CharField (max_length = 10, verbose_name = "Verification Code")
    mobile = models.CharField (max_length = 11, verbose_name = "phone")
    add_time = models.DateTimeField (default = datetime.now, verbose_name = "Add Time")
    class Meta:
        verbose_name = "SMS Verification"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code