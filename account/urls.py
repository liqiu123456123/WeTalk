# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
path('upload_file/', views.upload_file, name='upload_file'),
path('upload_img/', views.upload_image, name='upload_img'),
]