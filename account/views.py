from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth import authenticate

from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from account.models import MyUser


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MyUser.objects.get(Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:  #可以捕获除与程序退出sys.exit()相关之外的所有异常
            return None
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

        # Check for existing username
        if MyUser.objects.filter(username=username).exists():
            tips = '用户已存在'
            # Check for password consistency
        elif repeat_password != password:
            tips = '两次密码输入不一致'
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
