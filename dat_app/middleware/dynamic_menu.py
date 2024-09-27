from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in


# class M2(MiddlewareMixin):
#     def process_request(self, request):
#         # 只在用户登录时处理
#         if request.user.is_authenticated:
#             # 检查用户是否是超级管理员
#             is_superuser = User.objects.filter(username=request.user.username, is_superuser=True).exists()
#             # 需要限制的动态菜单
#
#             # 如果是超级管理员，添加菜单
#             if is_superuser:
#                 menus_admin = {
#                     'system_keep': True,
#                     'menu_display': ['用户管理', '任务列表'],
#                     'dynamic': False,
#                     'menus': [
#                         {
#                             'app': 'auth',
#                             'name': '用户管理',
#                             'icon': 'fa fa-th-list',
#                             'models': [
#                                 {
#
#                                     'name': '用户',
#                                     'url': 'auth/user',
#                                     'icon': 'fa fa-tasks',
#                                 },
#                                 {
#                                     'name': '组',
#                                     'url': 'auth/group',
#                                     'icon': 'fa fa-tasks',
#                                 },
#                             ]
#                         },
#                         {
#                             'name': '任务列表',
#                             'icon': 'fa fa-th-list',
#                             'models': [
#                                 {
#                                     'name': '任务介绍',
#                                     'url': '/introduction',
#                                     'icon': 'fa fa-tasks',
#                                 },
#                                 {
#                                     'name': '开始测试',
#                                     'url': '/index',
#                                     'icon': 'fa fa-tasks',
#                                 },
#                                 {
#                                     'name': '结果查询',
#                                     'url': '/results',
#                                     'icon': 'fa fa-tasks',
#                                 },
#                             ],
#                         },
#                     ]
#                 }
#
#                 settings.SIMPLEUI_CONFIG = menus_admin
#             # 如果不是超级管理员，移除菜单
#             else:
#                 menus_user = {
#                     'system_keep': True,
#                     'menu_display': ['用户管理', '任务列表'],
#                     'dynamic': False,
#                     'menus': [
#                         {
#                             'name': '任务列表',
#                             'icon': 'fa fa-th-list',
#                             'models': [
#                                 {
#                                     'name': '任务介绍',
#                                     'url': '/introduction',
#                                     'icon': 'fa fa-tasks',
#                                 },
#                                 {
#                                     'name': '开始测试',
#                                     'url': '/index',
#                                     'icon': 'fa fa-tasks',
#                                 },
#                                 {
#                                     'name': '结果查询',
#                                     'url': '/results',
#                                     'icon': 'fa fa-tasks',
#                                 },
#                             ],
#                         },
#                     ]
#                 }
#
#                 settings.SIMPLEUI_CONFIG["menus"] = menus_user

class M2(MiddlewareMixin):
    def process_request(self, request):
        is_superuser = User.objects.filter(username=request.user.username, is_superuser=True).exists()
        if is_superuser:
            settings.SIMPLEUI_CONFIG['menu_display'] = []
            menu_list = ["任务列表", "用户管理", "数据分析"]
            for menu in menu_list:
                settings.SIMPLEUI_CONFIG['menu_display'].append(menu)
        else:
            settings.SIMPLEUI_CONFIG['menu_display'] = []
            menu_list = ["任务列表"]
            for menu in menu_list:
                settings.SIMPLEUI_CONFIG['menu_display'].append(menu)
