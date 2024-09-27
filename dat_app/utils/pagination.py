""" 自定义分页组件 """
""" 以后若想要使用这个分页组件，你需要做这几个事情
在视图函数中：
    def num_list(request):
        # 1.根据自己情况筛选数据
        objs = models.PrettyNum.objects.filter(**data_dict).order_by("level")
        # 2.实例化分页对象
        page_object = Pagination(request,objs)
        # 3.分页后需要展示的数据
        objs = page_object.page_queryset
        # 4.分页后底部的页码信息
        page_str = page_object.page_str
        context = {
            "n1": objs,
            "n2": value,
            "n3": page_str,
        }
        return render(request, "num_list.html",context)
        
在html页面中：
    循环展示数据：
    {% for i in n1 %}
        <tr>
            <th>{{ i.id }}</th>
            <td>{{ i.mobile }}</td>
            <td>{{ i.price }} 元</td>
            <td>{{ i.get_level_display }}</td>
            <td>{{ i.get_status_display }}</td>
            <td>
                <a class="btn btn-primary btn-xs" href="/num/{{ i.id }}/edit">编辑</a>
                <a class="btn btn-danger btn-xs" href="/num/{{ i.id }}/delete">删除</a>
            </td>
        </tr>
    {% endfor %}
    页码功能：
    <ul class="pagination">
            {{ n3 }}
    </ul>
"""
from django.utils.safestring import mark_safe
import copy


class Pagination(object):

    def __init__(self, request, query_set, page_grarm="page", page_size=10):
        """

        :param request: 请求的对象
        :param query_set: 符合条件的数据（根据这个数据来进行分页处理）
        :param page_grarm: 在url传递获取分页的参数名
        :param page_size: 每页展示多少条数据
        """
        # 对原先url进行一个强复制
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_gram = page_grarm
        page = request.GET.get(page_grarm, "1")

        # 如果page是数字
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = query_set[self.start:self.end]

        # 自动增长的id
        for obj in self.page_queryset:
            obj.num = obj.pk

        total_count = query_set.count()
        total, div = divmod(total_count, page_size)
        if div:
            total += 1
        # 计算出当前页的前五页和后五页
        plus = 3
        if page > plus:
            start_page = page - plus
        else:
            start_page = 1
        if page + plus > total:
            end_page = total + 1
        else:
            end_page = page + plus + 1

        # 页码
        page_str_list = []

        # 已经把含有q值的url强复制下来，现在需要增加page的参数
        # 列表里面存放的为页码数
        # self.query_dict.setlist(self.page_gram,[page - 1])

        # 首页
        if page > 1:
            self.query_dict.setlist(self.page_gram, [1])
            prev = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(prev)

        # 上一页
        if page > 1:
            self.query_dict.setlist(self.page_gram, [page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(prev)

        # 循环多少次，则可以看到多少个页码
        for i in range(start_page, end_page):
            if i == page:
                self.query_dict.setlist(self.page_gram, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_gram, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

            # 下一页
        if page < total:
            self.query_dict.setlist(self.page_gram, [page + 1])
            nexv = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(nexv)

        # 尾页
        if page < total:
            self.query_dict.setlist(self.page_gram, [total])
            last = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(last)

        self.page_str = mark_safe("".join(page_str_list))
