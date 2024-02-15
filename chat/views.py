# chat/views.py
from django.shortcuts import render
from .models import ChatMessage
from account.models import MyUser
from django.http import JsonResponse
from django.db.models import Q


def user_chat_history(request, from_username, to_user_name):
    # 获取指定用户
    user = MyUser.objects.get(username=from_username)
    # 获取用户的id
    sender_id = user.id

    user = MyUser.objects.get(username=to_user_name)
    # 获取用户的id
    receiver_id = user.id

    messages = ChatMessage.objects.filter(
        Q(sender_id=sender_id, receiver_id=receiver_id) |  # 发送者是 send_id，接收者是 to_id
        Q(sender=receiver_id, receiver=sender_id)  # 或者发送者是 to_id，接收者是 send_id
    ).order_by('timestamp')  # 按时间戳排序
    for message in messages:
        print(
            f"From: {message.sender}, To: {message.receiver}, Content: {message.content}, Timestamp: {message.timestamp}")

        # 将消息列表转换为JSON格式
    messages_json = list(messages.values('sender__username', 'receiver__username', 'content', 'timestamp'))

    # 返回JSON响应
    return JsonResponse(messages_json, safe=False)

    # 渲染模板，并传递消息列表
    # return JsonResponse({'message': '注册激活码发送成功'}, status=200)
    # return render(request, 'chat/user_chat_history.html', {
    #     'sent_messages': sent_messages,
    #     'received_messages': received_messages,
    # })


def index_chat(request):
    return render(request, "chat_index.html")


def room(request, room_name):
    return render(request, "chat_room.html", {"room_name": room_name})
