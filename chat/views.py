# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "login.html")


def room(request, room_name):
    return render(request, "chat_room.html", {"room_name": room_name})