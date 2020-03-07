# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/12/2 12:56'

from rest_framework import serializers

from post.models import PostInfo, PostDetail
from material.serializers import SingleLevelCategorySerializer, TagSerializer, LicenseSerializer
from settings import MEDIA_URL_PREFIX


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostDetail
        fields = ('language', 'formatted_content', 'add_time', 'update_time')


class PostDetailInfoSerializer(serializers.ModelSerializer):
    category = SingleLevelCategorySerializer()
    tags = TagSerializer(many=True)
    license = LicenseSerializer()
    details = PostDetailSerializer(many=True)
    browse_auth = serializers.CharField(required=False, max_length=100, write_only=True)

    class Meta:
        model = PostInfo
        exclude = ('browse_password', 'browse_password_encrypt')


class PostBaseInfoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    front_image = serializers.SerializerMethodField()
    need_auth = serializers.SerializerMethodField()

    def get_front_image(self, post):
        if post.front_image:
            return "{0}/{1}".format(MEDIA_URL_PREFIX, post.front_image)

    def get_need_auth(self, post):
        if post.browse_password_encrypt:
            return True
        else:
            return False

    class Meta:
        model = PostInfo
        fields = (
            'id', 'title', 'en_title', 'desc', 'en_desc', 'author', 'tags', 'click_num', 'like_num', 'comment_num', 'post_type',
            'front_image', 'is_recommend', 'is_hot', 'is_banner', 'is_commentable', 'need_auth',
            'front_image_type', 'index', 'add_time')
