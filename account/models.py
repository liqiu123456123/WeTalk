from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image, ImageDraw, ImageFont
import io

class MyUser(AbstractUser):
    face_code = models.TextField(null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True,default=r'avatars\0.png')



    # 设置返回

