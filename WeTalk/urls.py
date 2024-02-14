# mysite/urls.py
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.urls import re_path
from django.views.static import serve
from chat import views
urlpatterns = [
    path("", include("account.urls")),
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
]