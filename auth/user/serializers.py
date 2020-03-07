#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 上午11:49
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : serializers.py
# @Software: PyCharm

import re
from datetime import datetime, timedelta
from rest_framework import serializers
from .models import GuestProfile, EmailVerifyRecord
from base.const import REGEX_EMAIL
from settings import REGEX_MOBILE
from user.models import VerifyCode
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()
class GuestSerializer(serializers.ModelSerializer):
    is_blogger = serializers.SerializerMethodField()

    def get_is_blogger(self, guest):
        if guest.email:
            return guest.email == '243316474@qq.com'
        else:
            return False

    class Meta:
        model = GuestProfile
        fields = ('id', 'nick_name', 'avatar', 'is_blogger')

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        Verify mobile number (function name must be validate_ + field name)
        """
        # Whether the phone is registered
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("User already exists")

        # Verify that the phone number is valid
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("Illegal mobile phone number")

        # Verification code sending frequency
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # Added more than a minute ago. Which is less than a minute from now
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("Less than 60s from the last transmission")

        return mobile

class EmailSerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50, min_length=1, required=True, label='昵称')
    email = serializers.EmailField(required=True, label='邮箱')

    def validate_email(self, email):
        """
        验证邮箱
        :param email:
        :return:
        """

        # 验证邮箱是否合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError("邮箱格式错误")

        # 验证发送频率
        ten_minutes_ago = datetime.now() - timedelta(hours=0, minutes=0, seconds=30)
        if EmailVerifyRecord.objects.filter(send_time__gt=ten_minutes_ago, email=email):
            raise serializers.ValidationError("请求发送过于频繁，请间隔30秒后重试")

        return email


class EmailVerifySerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50, min_length=1, required=True, label='昵称')
    email = serializers.EmailField(required=True, label='邮箱')
    code = serializers.CharField(max_length=4, min_length=4, required=False, label='验证码')

    def validate_email(self, email):
        """
        验证邮箱
        :param email:
        :return:
        """

        # 验证邮箱是否合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError("邮箱格式错误")

        return email
        
class MobileRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="Verification code",
                                 error_messages = {
                                     "blank": "Please enter a verification code",
                                     "required": "Please enter a verification code",
                                     "max_length": "Wrong captcha format",
                                     "min_length": "Wrong captcha format"
                                     },
                                 help_text="Verification code")
    username = serializers.CharField(label="username", help_text="username", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="User already exists")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="Password ", label =" password", write_only=True,
    )

    # Call the create method of the parent class, which will return the instantiated object of the current model, which is user.
    # # The former is to execute the original create of the parent class, and the latter is to add its own logic
    def create(self, validated_data):
        user = super(MobileRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):

        # getDifference from filter: There are two exceptions to get, one is multiple and one is none。
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # 验证码在数据库中是否存在，用户从前端post过来的值都会放入initial_data里面，排序(最新一条)。
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            # 获取到最新一条
            last_record = verify_records[0]

            # 有效期为五分钟。
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("Verification code expired")

            if last_record.code != code:
                raise serializers.ValidationError("Verification code error")

        else:
            raise serializers.ValidationError("Verification code error")

    #Validators without field names work on all fields. attrs is the total dict returned after the field validate
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
