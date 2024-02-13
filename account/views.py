import datetime
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from account.models import MyUser, EmailValid
import random
from django.core.mail import EmailMessage
from django.http import JsonResponse
from WeTalk.settings import MEDIA_ROOT
from .models import MyUser

def upload_file(request):
    if request.method == "POST":
        # 或者使用 items() 方法同时获取键和值
        print(request.user)
        file = request.FILES.get('file')
        file_path = os.path.join(MEDIA_ROOT, "avatars", file.name)
        with open(file_path, 'wb') as f:
            for i in file:
                f.write(i)
        my_user = MyUser.objects.get(username='liqile')

        # 更新 avatar 字段
        my_user.avatar = file.name

        # 保存对象
        my_user.save()
        return JsonResponse({'success': 'File uploaded successfully', })

    else:
        return JsonResponse({'error': 'File upload failed'}, status=400)


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MyUser.objects.get(Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:  # 可以捕获除与程序退出sys.exit()相关之外的所有异常
            return None


# 生成随机验证码的函数
def generate_verification_code(length=6):
    return ''.join(random.choices('0123456789', k=length))


def send_verification_code(request):
    # 获取请求中的邮箱地址
    email = request.POST.get('email')
    if not email:
        return JsonResponse({'error': 'Email is required.'}, status=400)

        # 生成验证码
    verification_code = generate_verification_code()

    # 存储验证码（例如，在用户的session中）
    request.session['verification_code'] = verification_code

    # 发送邮件
    subject = '注册激活码'
    body = f'你的注册激活码: {verification_code}'
    email_message = EmailMessage(subject, body, to=[email])
    email_message.send()

    e = EmailValid()  # 实例化表
    e.email_address = email  # 存入注册邮箱
    e.value = verification_code  # 存入验证码
    e.times = datetime.datetime.now()  # 存入时间
    e.save()  # 保存入数据库
    # 返回响应
    return JsonResponse({'message': '注册激活码发送成功'}, status=200)


@login_required
def index(request):
    return render(request, "index.html")


def user_login(request):
    # Initialize a dictionary to pass to the template
    context = {}
    # If the request is a POST, try to authenticate the user
    if request.method == 'POST':
        account = request.POST['email']
        password = request.POST['password']
        # Authenticate the user
        # 这里的username实际上是邮箱
        user = authenticate(request, username=account, password=password)
        # If authentication is successful, log the user in
        if user:
            login(request, user)
            # Redirect the user to the homepage or any other appropriate page
            return redirect(reverse('index'))
        else:
            # Authentication failed, update the context with error message
            context['error_message'] = '用户名或密码不正确'
            # If the request is not a POST, render the login form
    return render(request, 'login.html', context)


def register(request):
    confirmPassword = True
    tips = ""  # Initialize tips to None for clearer handling

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        repeat_password = request.POST.get('repeat_password', '')
        email_code = request.POST.get('email_verification_code', '')
        db_code = EmailValid.objects.filter(email_address=email).order_by('-times').first()
        # Check for existing username
        if MyUser.objects.filter(email=email).exists():
            tips = '邮箱已注册'
            # Check for password consistency
        elif repeat_password != password:
            tips = '两次密码输入不一致'
        elif email_code != db_code.value:
            tips = '验证码错误'
        else:
            # Create the user with the provided information
            try:
                user = MyUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    is_superuser=False,  # It's better to be explicit here
                    is_staff=False  # Ditto
                )
                tips = '注册成功，请登录'
                logout(request)  # Logout the current user (if any)
                return redirect(reverse('login'))
            except Exception as e:
                tips = f'注册失败: {str(e)}'

    return render(request, 'register.html', {'tips': tips, 'confirmPassword': confirmPassword})
