"""
URL configuration for dat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# 原本的路由

# 应用
from dat_app import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# ... the rest of your URLconf goes here ...


urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", views.datindex),
    path("introduction/", views.dat_introduction),
    path("results/", views.results_list),
    path("result/", views.results),
    path("dataAnalysis/", views.data_analysis),
    # path("spendtime/", views.spend_time),
    path("limitedtime/", views.get_limited_time),
    path("updatelimited/", views.update_limited_time),
    path("uploaduser/", views.upload_user),
    path("register/", views.register, name='registration'),
    path("login/", views.login),

    # 默认路由
    path('', views.redirect_to_admin),
]
# urlpatterns += staticfiles_urlpatterns()
