# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import xadmin
xadmin.autodiscover()
from rest_framework_swagger.views import get_swagger_view
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
schema_view = get_swagger_view(title='MYApi')

urlpatterns = [
    path('', schema_view),
    path('', include('api.urls')),
    path('admin/', xadmin.site.urls, name="admin"),
]+  aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# to load static/media files in development environment
