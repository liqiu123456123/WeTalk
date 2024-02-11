# mysite/urls.py
from django.contrib import admin
from django.urls import include, path
from chat import views
urlpatterns = [
    path("", include("account.urls")),
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),

]