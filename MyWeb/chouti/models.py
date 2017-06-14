from __future__ import unicode_literals

from django.db import models
# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(max_length=32, unique=True)
    image = models.ImageField(upload_to="user_image/%Y/%m", default="user_image/default.png", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class News(models.Model):
    category_choices = [
        (1, "42区"),
        (2, "段子"),
        (3, "图片"),
        (4, "挨踢1024"),
        (5, "你问我答")
    ]

    title = models.CharField(max_length=100, default="")
    summary = models.TextField(default="", max_length=500)
    href = models.URLField(max_length=100, default="")
    category = models.IntegerField(choices=category_choices)
    image = models.ImageField(upload_to="article_image/%Y/%m", default="article_image/default.png", max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)
    recommend = models.IntegerField(default=0)
    publisher = models.ForeignKey(UserInfo)

    class Meta:
        verbose_name = "新闻"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_comment_nums(self):
        return self.usercomment_set.all().count()


class UserComment(models.Model):
    new = models.ForeignKey(News)
    user = models.ForeignKey(UserInfo)
    content = models.CharField(max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey('UserComment', related_name='pid', null=True, blank=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class UserRecommend(models.Model):
    new = models.ForeignKey(News)
    user = models.ForeignKey(UserInfo)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "推荐"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    new = models.ForeignKey(News)
    user = models.ForeignKey(UserInfo)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = verbose_name


class ImageNews(models.Model):
    image = models.ImageField(upload_to="image_news/%Y/%m", max_length=100)
    desc = models.TextField(max_length=200, default="", blank=True, null=True)
    publisher = models.ForeignKey(UserInfo)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "图片新闻"
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    publisher = models.ForeignKey(UserInfo)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title