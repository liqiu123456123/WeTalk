from django.db import models
from account.models import MyUser


class Friendship(models.Model):
    # 用户发起好友请求的ID，指向User模型，当该Friendship记录被删除时，将级联删除相关的记录
    user_from = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='friendships_from')
    # 用户接收好友请求的ID，同样指向User模型，当该Friendship记录被删除时，将级联删除相关的记录
    user_to = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='friendships_to')
    message = models.TextField(max_length=500, blank=True)
    # 表示好友请求的状态，是一个最大长度为10的字符字段
    # 它有三个可能的值：'pending'（待处理），'accepted'（已接受），'rejected'（已阻止）
    status = models.CharField(max_length=10,
                              choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])

    # 用户发起好友请求的日期和时间，当该记录被创建时，Django会自动设置当前日期和时间
    date_requested = models.DateTimeField(auto_now_add=True)

    # 用户接受好友请求的日期和时间，如果好友请求尚未被接受，则为空
    # 当该字段为空时，Django的表单验证将忽略该字段，允许保存空值
    date_accepted = models.DateTimeField(null=True, blank=True)

    # 可以添加方法来处理好友请求，例如接受或拒绝
    def accept(self):
        self.status = 'accepted'
        self.save()
        # 这里可以添加逻辑来处理接受好友请求后的操作，例如建立双向好友关系

    def reject(self):
        self.status = 'rejected'
        self.save()
        # 这里可以添加逻辑来处理拒绝好友请求后的操作

    def get_from_user_username(self):
        return self.user_from.username

    def get_from_user_avatar(self):
        return self.user_from.avatar