from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User


# 检测是否存在登录的中间间
class M1(MiddlewareMixin):

    def process_request(self, request):

        # 获取当前用户请求的url
        # 如果为登录界面，不处理
        if request.path_info in ['/admin/login/', '/admin/logout/', '/admin/', '/register/']:
            return

        # 查询用户是否存在用户表中，如果是，则允许登录
        info = User.objects.filter(username=str(request.user)).exists()
        # print(info)
        if info:
            return
        else:
            return redirect("/admin/")
