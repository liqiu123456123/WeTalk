from django.db import models
from account.models import MyUser
class ChatMessage(models.Model):
    # 外键关联到发送者（User模型）
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='sent_messages')
    # 外键关联到接收者（User模型）
    receiver = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='received_messages')
    # 聊天记录内容
    content = models.TextField()
    # 聊天记录发送时间
    timestamp = models.DateTimeField(auto_now_add=True)

    # 可以添加其他字段，比如是否已读、聊天类型（私聊/群聊）等

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.content[:50]}"  # 限制显示内容长度
