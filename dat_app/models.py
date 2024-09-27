from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class dat_test(models.Model):
    username = models.CharField(max_length=32, default="", verbose_name="用户")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", null=True)
    word1 = models.CharField(max_length=32, default="", verbose_name="词汇1")
    word2 = models.CharField(max_length=32, default="", verbose_name="词汇2")
    word3 = models.CharField(max_length=32, default="", verbose_name="词汇3")
    word4 = models.CharField(max_length=32, default="", verbose_name="词汇4")
    word5 = models.CharField(max_length=32, default="", verbose_name="词汇5")
    word6 = models.CharField(max_length=32, default="", verbose_name="词汇6")
    word7 = models.CharField(max_length=32, default="", verbose_name="词汇7")
    word8 = models.CharField(max_length=32, default="", verbose_name="词汇8")
    word9 = models.CharField(max_length=32, default="", verbose_name="词汇9")
    word10 = models.CharField(max_length=32, default="", verbose_name="词汇10")
    dat_score = models.IntegerField(default=0, verbose_name="DAT得分")
    effective_num = models.IntegerField(default=0, verbose_name="有效词数")
    picture_path = models.CharField(verbose_name="图片地址", null=True, max_length=128)
    spend_time = models.CharField(verbose_name="作答时间", default='无', max_length=32)
    limited_time = models.CharField(verbose_name="限制时间",default='无',max_length=32)


class answer_log(models.Model):
    username = models.CharField(max_length=32, default="", verbose_name="用户")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    statue_choice = (
        (0, "开始作答"),
        (1, "结束作答"),
    )
    statue = models.SmallIntegerField(verbose_name="作答状态", choices=statue_choice)


class spend_time(models.Model):
    username = models.CharField(max_length=32, default="", verbose_name="用户名")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="作答开始时间")
    spend_time = models.CharField(verbose_name="作答时长", max_length=32)


class task_time(models.Model):
    task_name = models.CharField(max_length=32, verbose_name="发散性思维测试")
    limited_time = models.IntegerField(verbose_name="限制时间单位为s")
