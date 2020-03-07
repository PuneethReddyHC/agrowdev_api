from django.shortcuts import render
from random import choice


from settings import APIKEY
from rest_framework.response import Response
from rest_framework import viewsets, status
from  user.models import VerifyCode
from  user.serializers import SmsSerializer
from  utils.yunpian import YunPian
from rest_framework.mixins import CreateModelMixin
# Create your views here.
class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    sending text verify code
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        Generate a four-digit captcha string
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)

