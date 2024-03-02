import datetime
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import JsonResponse
from WeTalk.settings import MEDIA_ROOT
from .models import MyUser
from friendship.models import Friendship
import random
import string
import os  # 导入os库，用于操作文件
import cv2  # 导入cv2库，用于图像处理，例如绘制矩形框
from PIL import Image  # 导入PIL库中的Image模块，用于图像处理，例如绘制图片
import face_recognition  # 导入face_recognition库，用于人脸识别
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import base64
import numpy as np


@csrf_exempt  # 允许跨站请求伪造，仅用于测试环境
def upload_image(request):
    if request.method == 'POST':
        # 从请求中获取DataURL
        image_data = request.POST.get('image')
        # 移除DataURL的前缀
        image_data = image_data.split(',')[1]
        # 将DataURL解码为字节
        image_data = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_data))
        image.save("image/img_tmp.jpg")
        # 返回成功响应
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)



def upload_file(request):
    if request.method == "POST":
        # 或者使用 items() 方法同时获取键和值
        file = request.FILES.get('file')
        file_path = os.path.join(MEDIA_ROOT, "avatars", file.name)
        with open(file_path, 'wb') as f:
            for i in file:
                f.write(i)
        my_user = MyUser.objects.get(username='liqile')

        # 更新 avatar 字段
        my_user.avatar = os.path.join("avatars", file.name)

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

@login_required
def index(request):
    current_user = request.user
    user = MyUser.objects.get(username=current_user)
    user_id = user.id
    # 新好友请求
    pending_requests = Friendship.objects.filter(user_to_id=user_id, status='pending')
    # 联系人列表
    current_user_id = request.user.id
    # 使用Django的Q对象来构建复杂的查询条件
    friends = Friendship.objects.filter(
        Q(status='accept', user_from_id=current_user_id) |
        Q(status='accept', user_to_id=current_user_id)
    )
    messages = [
        {
            'content': '你好，我在等你发文件给我',
            'timestamp': '09:34'
        },
        {
            'content': '抱歉，现在我把文件发给你',
            'timestamp': '14:20'
        }
    ]

    context = {'pending_requests': pending_requests, 'current_user': current_user, 'friends': friends,'messages': messages}
    return render(request, 'index.html', context)


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
            return redirect(reverse('index'))
        else:
            context['error_message'] = '用户名或密码不正确'
    return render(request, 'login.html', context)

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def register(request):
    confirmPassword = True
    tips = ""  # Initialize tips to None for clearer handling
    if request.method == 'POST':
        username = generate_random_string(12)
        password = generate_random_string(12)
        tmp_img = r".\image\img_tmp.jpg"
        picture_of_tmp = face_recognition.load_image_file(tmp_img)
        try:
            face_encoding = face_recognition.face_encodings(picture_of_tmp)[0]
        except:
            print("没有检测到人脸，请重试")

        # 人脸特征数据存到myuser表中
        # 获取数据表中的人脸数据，逐个匹配，匹配到执行注册

        all_users = MyUser.objects.all()
        face_code_list = []
        #遍历所有记录并输出face_code字段
        for user in all_users:
            tmp = user.face_code
            tmp = tmp[1:-1]
            # 使用split方法按空格分割字符串
            list_data = tmp.split()
            # 将列表转换为NumPy数组
            np_array = np.array(list_data, dtype=float)
            face_code_list.append(np_array)

        results = face_recognition.compare_faces(face_code_list, face_encoding)
        if True in results:
            tips = '人脸已注册!请直接登录'
        else:
            # 创建新用户，存储人脸数据
            user = MyUser.objects.create_user(
                username=username,
                password=password,
                face_code=face_encoding,
                is_superuser=False,  # It's better to be explicit here
                is_staff=False,
            )
            tips = '注册成功，请登录'
            logout(request)
            return redirect(reverse('login'))
    return render(request, 'register.html', {'tips': tips, 'confirmPassword': confirmPassword})
