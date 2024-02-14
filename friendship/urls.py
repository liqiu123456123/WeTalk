# urls.py
from django.urls import path
from . import views  # 导入你的视图

urlpatterns = [
    # ... 其他路由 ...
    path('add-friend/', views.add_friend, name='add_friend'),
    path('accept-friend/', views.accept_friend, name='accept_friend'),
    # ... 其他路由 ...
]