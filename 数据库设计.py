
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# 自定义用户模型，继承自AbstractUser
class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    # 可以添加其他自定义字段

    def __str__(self):
        return self.username

    # 好友关系模型


class Friendship(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_to')
    status = models.CharField(max_length=10,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('blocked', 'Blocked')])
    date_requested = models.DateTimeField(auto_now_add=True)
    date_accepted = models.DateTimeField(null=True, blank=True)


# 消息模型
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True, related_name='messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    chat_type = models.CharField(max_length=10, choices=[('private', 'Private'), ('group', 'Group')])


# 群组模型
class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_admin')
    members = models.ManyToManyField(User, through='GroupMember', related_name='groups')


# 群组成员模型
class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('member', 'Member'), ('admin', 'Admin')])
    date_joined = models.DateTimeField(auto_now_add=True)


# 聊天会话模型
class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_user2')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='group_chats')
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='last_in_chat')
    date_last_message = models.DateTimeField(null=True, blank=True)
    is_group = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user1', 'user2'),)

    def save(self, *args, **kwargs):
        if not self.is_group:
            self.group = None
        super().save(*args, **kwargs)








"""

创建一个类似于微信的社交网站需要仔细规划数据库结构，以确保高效的数据存储和查询。以下是一个简化的数据库设计示例，这个设计涵盖了用户、
好友关系、消息、群组、个人信息等基础功能。请注意，实际开发中可能需要更多的表和字段来支持更复杂的功能。

用户表（User）
id (用户ID，主键，自增)
username (用户名，唯一索引)
password (加密后的密码)
email (邮箱地址，唯一索引)
phone_number (手机号，唯一索引)
profile_picture (头像图片的URL)
bio (个人简介)
date_joined (加入日期)
last_login (最后登录日期)
is_active (用户状态，是否活跃)
is_staff (是否为管理员)
好友关系表（Friendship）
id (好友关系ID，主键，自增)
user_from (用户ID，发起好友请求的用户)
user_to (用户ID，接收好友请求的用户)
status (关系状态，例如：pending, accepted, blocked)
date_requested (请求日期)
date_accepted (接受日期)
消息表（Message）
id (消息ID，主键，自增)
sender_id (发送者用户ID)
receiver_id (接收者用户ID)
content (消息内容)
date_sent (发送日期)
is_read (消息是否已读)
chat_type (聊天类型，例如：private, group)
chat_id (聊天ID，用于区分不同的聊天会话)
群组表（Group）
id (群组ID，主键，自增)
name (群组名称)
description (群组描述)
admin_id (群主用户ID)
date_created (创建日期)
群组成员表（GroupMember）
id (成员ID，主键，自增)
group_id (群组ID)
user_id (用户ID)
role (成员角色，例如：member, admin)
date_joined (加入群组日期)
聊天会话表（Chat）
id (聊天会话ID，主键，自增)
user_id1 (用户ID1，用于区分两个用户之间的聊天)
user_id2 (用户ID2)
last_message_id (最后一条消息的ID)
date_last_message (最后一条消息日期)
is_group (是否为群组聊天，布尔值)
请注意，以上设计只是一个基础版本，并且没有涵盖所有的功能和细节。例如，你可能还需要考虑用户的在线状态、文件传输、朋友圈、动态、通知、隐私设置、
黑名单等功能，这些功能都需要额外的表和字段来支持。

另外，对于密码和其他敏感信息，务必使用安全的加密方法存储。Django提供了内置的用户认证系统，可以方便地处理用户注册、登录和权限管理等功能，
你也可以在此基础上进行扩展和定制。

在开发过程中，建议经常进行数据库优化和索引调整，以提高查询性能和用户体验。同时，也要考虑数据库的可扩展性和维护性，以便在网站规模扩大或功能
增加时能够轻松地进行扩展和升级。


"""