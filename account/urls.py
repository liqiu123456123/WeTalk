# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path('send_code/', views.send_verification_code, name='send_verification_code'),
path('upload_file_ajax/', views.upload_file_ajax, name='upload-file-ajax'),
]