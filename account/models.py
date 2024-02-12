from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    name = models.CharField('姓名', max_length=50, default='匿名用户')
    introduce = models.TextField('简介', default='暂无介绍')
    company = models.CharField('公司', max_length=100, default='暂无信息')
    profession = models.CharField('职业', max_length=100, default='暂无信息')
    telephone = models.CharField('电话', max_length=11, default='暂无信息')
    photo = models.ImageField('头像', blank=True, upload_to='images/user/')
    email = models.EmailField('邮箱', max_length=100, blank=True, default='')

    # 设置返回值
    def __str__(self):
        return self.name
