from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
# Create your views here.
from  user_operation.models import UserFav, UserLeavingMessage, UserAddress
from  user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, \
    AddressSerializer
from rest_framework.permissions import IsAuthenticated
from  utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class UserFavViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    """
    list:
        Get user favorite list
    retrieve:
        Determine if a product is already favorited
    create:
        Favorite Product
    """
    # queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    lookup_field = 'products_id'
    # lookup_field = 'products'
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 收藏数+1
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     # 通过这个instance Userfav找到products
    #     products = instance.products
    #     products.fav_num +=1
    #     products.save()

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 设置动态的Serializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        Get user message
    create:
        Add message
    delete:
        Delete message function
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    # 只能看到自己的留言
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """
    Shipping address management
    list:
        Get shipping address
    create:
        Add shipping address
    update:
        Update shipping address
    delete:
        Delete shipping address
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
