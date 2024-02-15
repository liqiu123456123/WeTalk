# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_chat, name="chat"),
    path("<str:room_name>/", views.room, name="room"),
    path('history/<str:from_username>/<str:to_user_name>/', views.user_chat_history, name='user_chat_history'),
]