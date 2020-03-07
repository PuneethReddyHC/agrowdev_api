from django.db import models


class QiniuTokenRecord(models.Model):
     """
     Seven Cow Cloud Requests Token
     """
     CODE_TYPE = (
         ("comment", "comment"),
     )

     ip = models.GenericIPAddressField(blank = False, null = False, verbose_name = "Requester IP", help_text = "Requester IP")
     token = models.CharField(max_length = 512, verbose_name = "token", help_text = "token")
     use_type = models.CharField(max_length = 15, choices = CODE_TYPE, verbose_name = "use type", help_text = "use type")
     add_time = models.DateTimeField(auto_now_add = True, verbose_name = "send time", help_text = "send time")

     def __str__ (self):
         return '{0} [{1}]'. format (self.ip, self.token)

     class Meta:
         verbose_name = "Qiniu Cloud Requests Token"
         verbose_name_plural = verbose_name