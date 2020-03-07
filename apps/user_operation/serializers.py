# encoding: utf-8
from rest_framework.validators import UniqueTogetherValidator

__author__ = 'puneeth'
__date__ = '2018/3/10 0010 09:54'
from rest_framework import serializers
from  user_operation.models import UserFav, UserLeavingMessage, UserAddress
from  products.serializers import ProductsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    # 通过products_id拿到商品信息。就需要嵌套的Serializer
    products = ProductsSerializer()

    class Meta:
        model = UserFav
        fields = ("products", "id")

class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        # 使用validate方式实现唯一联合
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'products'),
                message="Favorited"
            )
        ]

        fields = ("user", "products", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")
