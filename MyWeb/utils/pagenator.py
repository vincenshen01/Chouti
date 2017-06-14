"""
使用方法：
    all_count = Models.objects.all().count()
    page_info = Paginator(request.GET.get("p"), 10, all_count, request.path_info)
    host_obj = Models.objects.all()[page_info.start: page_info.end]
"""


class Paginator(object):
    def __init__(self, current_page, per_page_number, all_data_count, base_url, page_range=5):
        """
        :param current_page: 当前页
        :param per_page_number: 每页显示的数据条数
        :param all_data_count: 数据库中数据的总条数
        :param base_url: 页面的前缀
        :param page_range: 页码的显示范围
        """
        try:
            current_page = int(current_page)
        except Exception:
            current_page = 1
        self.current_page = current_page
        self.per_page_number = per_page_number
        self.all_data_count = all_data_count
        self.base_url = base_url
        self.page_range = page_range
        a, b = divmod(all_data_count, per_page_number)
        if b == 0:
            self.all_page = a
        else:
            self.all_page = a + 1

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_number

    @property
    def end(self):
        return self.current_page * self.per_page_number

    def page_str(self):
        """
        在HTML页面中显示页码标签
        :return:
        """
        page_html = []

        # 上一页逻辑
        if self.current_page <= 1:
            prev = '<li><a href="#">首页</a></li>'
        else:
            prev = '<li><a href="%s?p=%s">上一页</a></li>' % (self.base_url, self.current_page - 1)
        page_html.append(prev)

        # 页码逻辑
        if self.all_page <= self.page_range:
            start = 1
            end = self.all_page + 1
        else:
            if self.current_page > int(self.page_range / 2):
                if (self.current_page + int(self.page_range / 2)) > self.all_page:
                    start = self.all_page - self.page_range + 1
                    end = self.all_page + 1
                else:
                    start = self.current_page - int(self.page_range / 2)
                    end = self.current_page + int(self.page_range / 2) + 1
            else:
                start = 1
                end = self.page_range + 1
        for i in range(start, end):
            if self.current_page == i:
                page_number = '<li class="active"><a href="%s?p=%s">%s</a></li>' % (self.base_url, i, i)
            else:
                page_number = '<li><a href="%s?p=%s">%s</a></li>' % (self.base_url, i, i)
            page_html.append(page_number)

        # 下一页逻辑
        if self.current_page >= self.all_page:
            nex = '<li><a href="#">尾页</a></li>'
        else:
            nex = '<li><a href="%s?p=%s">下一页</a></li>'
        page_html.append(nex)

        return "&nbsp;&nbsp;".join(page_html)