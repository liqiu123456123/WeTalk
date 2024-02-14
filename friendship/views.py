# views.py  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Friendship
from django.http import JsonResponse
from account.models import MyUser
from django.db.models import F
from django.utils import timezone
from django.db.models import Case, Value, When, F
from django.db import models
@login_required  # 确保用户已登录
def add_friend(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            friend = MyUser.objects.get(email=email)
            # 创建好友请求  
            request = Friendship.objects.create(
                user_from=request.user,
                user_to=friend,
                message=request.POST.get('message', ''),
                status='pending'
            )
            # 可以发送通知给好友  
            # ...  
            return JsonResponse({'message': '注册激活码发送成功'}, status=200)
        except User.DoesNotExist:
            # 好友用户名不存在  
            error_message = '用户不存在，请检查用户名并重试。'


@login_required
def accept_friend(request):
    if request.method == 'POST':
        # 查询最新的添加好友记录，from_id,to_id
        from_id = request.POST.get('user_from_id')
        to_id = request.POST.get('user_to_id')
        # 假设你要将status更新为'pending'
        new_status = 'accept'
        print("form_id", from_id)
        print("to_id", to_id)
        # 构建条件更新表达式
        condition = Case(
            When(date_accepted__isnull=False, then=F('date_accepted')),  # 如果date_accepted不为空，使用当前值
            default=Value(timezone.now()),  # 如果date_accepted为空，使用当前时间
            output_field=models.DateTimeField()  # 指定输出字段的类型
        )

        # 执行更新操作
        Friendship.objects.filter(user_to_id=to_id, user_from_id=from_id).update(
            status=new_status,
            date_accepted=condition
        )
        # # 使用update方法来更新匹配的记录
        # Friendship.objects.filter(user_to_id=to_id, user_from_id=from_id).update(status=new_status,
        #                                                                          date_accepted=F('date_accepted') if F(
        #                                                                              'date_accepted') is not None else timezone.now()
        #                                                                          # 如果date_accepted已经设置，则保持不变，否则设置为当前时间
        #                                                                          )
        return JsonResponse({'message': '同意'}, status=200)


@login_required
def friend_requests(request):
    pending_requests = Friendship.objects.filter(user_to_id=request.user, status='pending')
    context = {'pending_requests': pending_requests}
    return render(request, 'index.html', context)
