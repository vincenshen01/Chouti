from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from utils.baseresponse import AjaxResponse
# Create your views here.
from .forms import RegisterForm, LoginForm, ImageNewsForm
from .models import UserInfo, News, UserRecommend, UserComment, Article
from utils.pagenator import Paginator
from utils.identify_code import create_validate_code
from io import BytesIO
from django.db.models import F
import os
import uuid
import json
from datetime import datetime
from django.conf import settings


class IndexView(View):
    """
    主页视图
    """
    def get(self, request):
        register_obj = RegisterForm()
        login_obj = LoginForm()
        news_count = News.objects.all().count()
        paginator = Paginator(request.GET.get("p"), 4, news_count, request.path_info)
        news = News.objects.all().order_by("-add_time")[paginator.start: paginator.end]
        return render(request, "index.html", {
            "register_obj": register_obj,
            "login_obj": login_obj,
            "news": news,
            "paginator": paginator,
        })


class UserCommentView(View):
    """
    用户评论视图
    """
    response = AjaxResponse()

    def get(self, request, news_id):
        comment_list = UserComment.objects.filter(new_id=news_id).values()

        # 将queryset列表中的元素增加child：[], 并将其按照id转换为字典。
        comment_dict = {}
        for row in comment_list:
            row['child'] = []
            comment_dict[row['id']] = row

        # 将queryset列表中有的parent_id_id的元素添加到父元素的child中。
        for row in comment_list:
            if row['parent_id_id']:
                parent_id_id = row['parent_id_id']
                comment_dict[parent_id_id]['child'].append(row)

        comment_result = {}
        for k, v in comment_dict.items():
            if v['parent_id_id'] is None:
                comment_result[k] = v
        cmt_str = self.create_comment_html(comment_result)
        self.response.data = cmt_str
        return HttpResponse(json.dumps(self.response.__dict__))

    def post(self, request):
        news_id = request.POST.get("news_id", "")
        user_id = request.session.get("id", "")
        content = request.POST.get("content", "")
        UserComment.objects.create(new_id=news_id, user_id=user_id, content=content)
        return HttpResponse(json.dumps(self.response.__dict__))

    def create_comment_html(self, comment_result):
        prev = """
        <div class="comment">
            <div class="content">
        """
        end = """
            </div>
        </div>
        """
        for k, v in comment_result.items():
            content = '<div class="item">--%s</div>' % v['content']
            prev += content
            if v['child'] is not None:
                node = self.create_child_node(v['child'])
                prev += node
        return prev + end

    def create_child_node(self, child_comment):
        prev = """
                <div class="comment">
                    <div class="content">
                """
        end = """
                    </div>
                </div>
                """
        for child in child_comment:
            content = '<div class="item">--%s</div>' % child['content']
            prev += content
            if child['child'] is not None:
                node = self.create_child_node(child['child'])
                prev += node
        return prev + end


class RegisterView(View):
    """
    注册视图
    """
    def post(self, request):
        register_obj = RegisterForm(request.POST)
        response = AjaxResponse()
        if register_obj.is_valid():
            register_obj.save(commit=True)
        else:
            response.status = False
            response.error = register_obj.errors
        return HttpResponse(json.dumps(response.__dict__))


class LoginView(View):
    """
    登录视图
    """
    def post(self, request):
        response = AjaxResponse()
        code = request.POST.get("code", "")

        if code.upper() == request.session['identify_code'].upper():
            login_obj = LoginForm(request.POST)
            if login_obj.is_valid():
                user_obj = UserInfo.objects.filter(username=login_obj.cleaned_data["login_username"],
                                                   password=login_obj.cleaned_data["login_password"]).first()
                if user_obj:
                    request.session["id"] = user_obj.id
                    request.session["username"] = user_obj.username
                else:
                    response.status = False
                    response.error = "用户名或密码错误"
            else:
                response.status = False
                response.error = "用户名或密码错误"
        else:
            response.status = False
            response.error = "验证码错误"
        return HttpResponse(json.dumps(response.__dict__))


class LogoutView(View):
    """
    注销视图
    """
    def get(self, request):
        request.session.flush()
        return redirect(reverse("index"))


class RecommendView(View):
    """
    点赞视图
    """
    def post(self, request):
        user = request.session.get("username", "")
        user_obj = UserInfo.objects.get(username=user)
        news_id = request.POST.get("news_id", "")
        recommend = UserRecommend.objects.filter(user=user_obj, new_id=news_id)
        if recommend.exists():
            recommend.delete()
            News.objects.filter(id=news_id).update(recommend=F("recommend")-1)
            return HttpResponse(json.dumps(0))
        else:
            UserRecommend.objects.create(user=user_obj, new_id=news_id)
            News.objects.filter(id=news_id).update(recommend=F("recommend")+1)
            return HttpResponse(json.dumps(1))


class AjaxUploadImageView(View):
    """
    ajax上传图片
    """
    def post(self, request):
        response = AjaxResponse()
        try:
            image_form = ImageNewsForm(request.POST, request.FILES)
            user = request.session.get("username", "")
            user_obj = UserInfo.objects.get(username=user)
            if image_form.is_valid():
                title = request.POST.get("title")
                if title:
                    image_url = request.POST.get("image_url")
                    news = News.objects.filter(image=image_url)
                    news.update(title=title, href=image_url)
                    response.index = True
                else:
                    image_obj = News.objects.create(image=image_form.cleaned_data["image"], publisher=user_obj, category=3)
                    response.data = str(image_obj.image)
            else:
                response.status = False
                response.error = "上传失败"
        except Exception as e:
            response.status = False
            response.error = "上传失败"
        return HttpResponse(json.dumps(response.__dict__))


class IdentifyCodeView(View):
    """
    验证码生成视图
    """
    def get(self, request):
        img_obj, code = create_validate_code()
        stream = BytesIO()
        img_obj.save(stream, 'png')
        request.session['identify_code'] = code
        return HttpResponse(stream.getvalue())


class UploadImageView(View):
    """
    富文本图片上传
    """
    def post(self, request):
        images_dir = "kind_editor_upload_images"
        result = {'error': 1, 'message': '上传出错'}
        image = request.FILES.get('imgFile', None)
        if image:
            result = self.image_upload(image, images_dir)
        return HttpResponse(json.dumps(result))

    def image_upload(self, image, images_dir):
        """
        图片上传
        :param image: 接收图片文件
        :param images_dir: 接收图片上传根目录
        :return: 返回图片url
        """
        allow_suffix = ['jpg', 'png', 'jpeg', 'git', 'bmp']     # 允许上传的图片类型
        image_suffix = image.name.split('.')[-1]
        if image_suffix not in allow_suffix:
            return {'error': 1, 'message': '图片格式不正确'}
        relative_file_path = self.image_dir(images_dir)
        dir_path = os.path.join(settings.MEDIA_ROOT, relative_file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        image_name = str(uuid.uuid1()) + '.' + image_suffix
        image_path = os.path.join(dir_path, image_name)
        image_url = settings.MEDIA_URL + relative_file_path + image_name
        open(image_path, 'wb').write(image.file.read())
        return {'error': 0, 'url': image_url}

    def image_dir(self, images_dir):
        """
        生成图片目录
        :param images_dir: 接收图片上传根目录
        :return: 返回当前日期生成的图片目录
        """
        today = datetime.today()
        images_dir += '/%d/%d/' % (today.year, today.month)
        return images_dir


class ArticleView(View):
    def get(self, request):
        articles = Article.objects.all()
        return render(request, "kindeditor.html", {"articles": articles})

    def post(self, request):
        title = request.POST.get("title", "")
        publisher_id = 1
        content = request.POST.get("content", "")
        Article.objects.create(title=title, publisher_id=publisher_id, content=content)
        return redirect(reverse("article"))
