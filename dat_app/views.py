from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django import forms
from dat_app import models
from django.contrib.auth.models import User
from dat_app.utils.dat_test import count_dat
from dat_app.utils.pagination import Pagination
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserCreationForm
import time
import os
import pandas as pd
from django.contrib import messages


# Create your views here.

# dat任务介绍
def dat_introduction(request):
    return render(request, "introduction.html")


# 注册
# modelform
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # 在这里设置is_staff字段
            user.is_staff = True  # 或根据你的业务逻辑设置为 False
            # 现在保存用户
            user.save()
            # form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    return render(request, 'admin/login.html')


# dat任务测试功能
class datModelForm(forms.ModelForm):
    class Meta:
        model = models.dat_test
        fields = ["word1", "word2", "word3", "word4", "word5", "word6", "word7", "word8", "word9", "word10"]

    # 添加自定义样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 用于添加渲染标签，视情况保留
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": "请输入名词..."}


@csrf_exempt
def datindex(request):
    # 请求时，渲染数据表单
    if request.method == "GET":
        form = datModelForm
        # 保存一个用户点击开始作答的log
        record = models.answer_log(username=str(request.user), statue=0)
        record.save()
        limited_time = models.task_time.objects.filter(task_name='DAT').first()
        return render(request, "dat_test.html", {"time": limited_time.limited_time})

    # 通过post请求提交数据，进行结果查看，此时返回
    elif request.method == "POST":
        try:
            word1 = request.POST.get("word1")
            word2 = request.POST.get("word2")
            word3 = request.POST.get("word3")
            word4 = request.POST.get("word4")
            word5 = request.POST.get("word5")
            word6 = request.POST.get("word6")
            word7 = request.POST.get("word7")
            word8 = request.POST.get("word8")
            word9 = request.POST.get("word9")
            word10 = request.POST.get("word10")
            limTime = request.POST.get("limitedTime")
            instance = models.dat_test.objects.create(word1=word1, word2=word2,
                                                      word3=word3, word4=word4,
                                                      word5=word5, word6=word6,
                                                      word7=word7, word8=word8,
                                                      word9=word9, word10=word10,
                                                      username=str(request.user),
                                                      spend_time=request.POST.get("spendtime"),
                                                      limited_time=limTime,
                                                      )
            instance.save()
            data_dict = {"word1": word1, "word2": word2, "word3": word3, "word4": word4, "word5": word5, "word6": word6,
                         "word7": word7, "word8": word8, "word9": word9, "word10": word10}
            # 计算得分
            respond_dict = count_dat(data_dict, str(request.user))
            instance.dat_score = respond_dict["dat_score"]
            instance.effective_num = respond_dict["effective_num"]
            instance.picture_path = respond_dict["filepath"]
            instance.save()
            # 后面取消返回内容
            return JsonResponse(respond_dict)
        except:
            return HttpResponse("请求异常!")


@csrf_exempt
# 根据用户查询作答记录
def results_list(request):
    if request.method == "GET":
        is_superuser = User.objects.filter(username=request.user.username, is_superuser=True).exists()
        if is_superuser:
            queryset = models.dat_test.objects.all()

            # 添加自动增加序号
            # data = []
            # for i, item in enumerate(queryset, start=1):
            #     data.append({'item': item, 'num': i})
            # num_list = list(range(1, len(queryset)+1))

            object1 = Pagination(request, queryset)
            departs = object1.page_queryset
            pagestr = object1.page_str

            # 搜索框
            show_search_box = True

            return render(request, "results.html", {"n1": departs, "n3": pagestr, "show_search_box": show_search_box})
        else:
            queryset = models.dat_test.objects.filter(username=str(request.user))
            object1 = Pagination(request, queryset)
            departs = object1.page_queryset
            pagestr = object1.page_str

            # 搜索框
            show_search_box = False

            return render(request, "results.html", {"n1": departs, "n3": pagestr, "show_search_box": show_search_box})

    elif request.method == "POST":
        is_superuser = User.objects.filter(username=request.user.username, is_superuser=True).exists()
        if is_superuser:
            query_param = request.POST.get('query_param')
            # 根据输入的内容判断是按照 ID 还是用户名查询

            results = models.dat_test.objects.filter(username=query_param)

            object1 = Pagination(request, results)
            departs = object1.page_queryset
            pagestr = object1.page_str

            # 搜索框
            show_search_box = True

            return render(request, "results.html", {"n1": departs, "n3": pagestr, "show_search_box": show_search_box})


# 计算百分比的函数
def calculate_percentage(numerator, denominator):
    quotient, _ = divmod(numerator, denominator)
    percentage = round(quotient * 100)
    return percentage


# 查看记录
@csrf_exempt
def results(request):
    id = request.POST.get("id")
    if request.method == "POST":
        try:
            # 获取数据
            queryset = models.dat_test.objects.filter(id=id).first()
            # 获取图片地址
            pic_path = queryset.picture_path
            # 获取得分
            dat_score = queryset.dat_score
            # 获取作答记录信息
            field1 = queryset.word1
            field2 = queryset.word2
            field3 = queryset.word3
            field4 = queryset.word4
            field5 = queryset.word5
            field6 = queryset.word6
            field7 = queryset.word7
            field8 = queryset.word8
            field9 = queryset.word9
            field10 = queryset.word10
            response_word = f'{field1},{field2},{field3},{field4},{field5},{field6},{field7},{field8},{field9},{field10}'
            # 超越了多少人
            all_data = models.dat_test.objects.all()
            scores = all_data.values('dat_score')
            scores_list = []
            for score in scores:
                scores_list.append(score["dat_score"])
            smaller = []
            for score in scores_list:
                if score < int(dat_score):
                    smaller.append(score)
            # 超越了多少人
            percentage = (len(smaller) / len(scores_list)) * 100

            data = {'image_url': pic_path, "dat_score": dat_score, "response_word": response_word,
                    "percentage": percentage}
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
        except:
            return JsonResponse({'error': 'Item not found'}, status=404)


# 数据分析
@csrf_exempt
def data_analysis(request):
    factor = User.objects.filter(username=request.user, is_superuser=1).exists()
    if factor:
        # 当请求为get时，给出描述性数据分析
        if request.method == "GET":
            try:
                data = models.dat_test.objects.filter(~Q(username='')).values_list('dat_score')
                score_list = []
                for value in data:
                    score_list.append(int(value[0]))

                min_score = min(score_list)
                max_score = max(score_list)
                # 平均分
                avg_score = np.mean(score_list)
                # 中位数
                media_score = np.median(score_list)
                # 极差
                ptp_score = np.ptp(score_list)
                # 方差
                var_score = np.var(score_list)
                # 标准差
                std_score = np.std(score_list)

                context = {"max": max_score, "min": min_score, "avg": avg_score, "media": media_score, "ptp": ptp_score,
                           "var": var_score, "std": std_score}

                return render(request, "data_analysis.html", context)

            except:
                return render(request, "403.html")

        # 当请求为post的时候，用于传输echatrt图表
        else:
            data = models.dat_test.objects.filter(~Q(username='')).values_list('dat_score')
            score_list = []
            for value in data:
                score_list.append(int(value[0]))

            score_range = ['<30', '30-40', '40-50', '50-60', '60-70', '>70']
            s30 = 0
            s30_40 = 0
            s40_50 = 0
            s50_60 = 0
            s60_70 = 0
            s70 = 0

            for score in score_list:
                if score < 30:
                    s30 += 1
                elif score >= 30 and score < 40:
                    s30_40 += 1
                elif score >= 40 and score < 50:
                    s40_50 += 1
                elif score >= 50 and score < 60:
                    s50_60 += 1
                elif score >= 60 and score < 70:
                    s60_70 += 1
                elif score >= 70:
                    s70 += 1

            data = {
                # 柱状图
                "bar": {
                    'xAxis': {
                        'type': 'category',
                        'data': score_range
                    },
                    'yAxis': {
                        'type': 'value'
                    },
                    'series': [
                        {
                            'data': [s30, s30_40, s40_50, s50_60, s60_70, s70],
                            'type': 'bar'
                        }
                    ]
                },
                # 箱型图
                "boxplot": {
                    'title': [
                        {
                            'text': '箱型图',
                            'left': 'center'
                        },
                        # {
                        #     # 'text': 'upper: Q3 + 1.5 * IQR \nlower: Q1 - 1.5 * IQR',
                        #     'borderColor': '#999',
                        #     'borderWidth': 1,
                        #     'textStyle': {
                        #         'fontWeight': 'normal',
                        #         'fontSize': 14,
                        #         'lineHeight': 20
                        #     },
                        #     'left': '10%',
                        #     'top': '90%'
                        # }
                    ],
                    'dataset': [
                        {
                            'source': [
                                score_list
                            ]
                        },
                        {
                            'transform': {
                                'type': 'boxplot',
                                'config': {'itemNameFormatter': 'dat_score {value}'}
                            }
                        },
                        {
                            'fromDatasetIndex': 1,
                            'fromTransformResult''': 1
                        }
                    ],
                    'tooltip': {
                        'trigger': 'item',
                        'axisPointer': {
                            'type': 'shadow'
                        }
                    },
                    'grid': {
                        'left': '10%',
                        'right': '10%',
                        'bottom': '15%'
                    },
                    'xAxis': {
                        'type': 'category',
                        'boundaryGap': 'true',
                        'nameGap': 30,
                        'splitArea': {
                            'show': 'false'
                        },
                        'splitLine': {
                            'show': 'false'
                        }
                    },
                    'yAxis': {
                        'type': 'value',
                        'name': 'score',
                        'splitArea': {
                            'show': 'true'
                        }
                    },
                    'series': [
                        {
                            'name': 'boxplot',
                            'type': 'boxplot',
                            'datasetIndex': 1
                        },
                        {
                            'name': 'outlier',
                            'type': 'scatter',
                            'datasetIndex': 2
                        }
                    ]
                },

            }

            return JsonResponse(data)
    else:
        return render(request, "403.html")


@csrf_exempt
@require_http_methods(["POST"])
def spend_time(request):
    if request.method == "POST":
        data = request.POST
        # print(data)
        # 单位为秒
        spend_time = data.get('spendtime')
        start_time = data.get('starttime')
        # 将开始时间还原为时间
        record = models.spend_time(username=request.user, spend_time=spend_time)
        record.save()
        return JsonResponse(data)


# 访问ip时，直接重定向到admin
def redirect_to_admin(request):
    return redirect('/admin')


@require_http_methods(["GET"])
def get_limited_time(request):
    if request.method == "GET":
        limited_time = models.task_time.objects.filter(task_name='DAT').first()
        data_dict = {
            "limited_time": limited_time.limited_time
        }
        return JsonResponse(data_dict)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def update_limited_time(request):
    factor = User.objects.filter(username=request.user, is_superuser=1).exists()
    if factor:
        if request.method == "GET":
            return render(request, "update.html")
        elif request.method == "POST":
            try:
                data = request.POST
                number = data.get('number')
                models.task_time.objects.filter(task_name='DAT').update(limited_time=number)
                return JsonResponse({'message': 'success'}, status=200)
            except:
                return JsonResponse({'message': 'fail'}, status=404)
    else:
        return render(request, "403.html")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def upload_user(request):
    factor = User.objects.filter(username=request.user, is_superuser=1).exists()
    if factor:
        if request.method == "GET":
            return render(request, "upload_user.html")
        elif request.method == "POST":
            # 尝试读取文件，若读取成功进入下一步
            try:
                for key, filedata in request.FILES.items():
                    # 判断文件是否符合格式
                    filename = filedata.name
                    extension = os.path.splitext(filename)
                    # print(type(extension[1]))
                    if extension[1] != '.xlsx' and extension[1] != '.xls':
                        return JsonResponse({"results": "文件格式不正确！"})
                    else:
                        df = pd.read_excel(filedata)
                        data = df.to_dict(orient='records')
                        # print(data)
                        results = ''
                        for data_dict in data:
                            username = data_dict["username"]
                            instance = User.objects.filter(username=username).exists()

                            # 判断是否为已存在的用户
                            if instance:
                                results += str(username)
                                results += ' '
                            else:
                                user = User.objects.create_user(username=data_dict["username"],
                                                                password=str(data_dict["password"]),
                                                                first_name=data_dict["name"],
                                                                is_staff=1)
                        # a = JsonResponse({"results": "文件上传成功！"})
                        # a.status_cod = 200
                        if results == '':
                            content = {"results": "文件上传成功"}
                        else:
                            content = {"results": "文件上传成功。" + str(results) + "这些用户已存在"}
                        return JsonResponse(content)
            except:
                return JsonResponse({"results": "文件上传失败！"})
    else:
        return render(request, "403.html")
