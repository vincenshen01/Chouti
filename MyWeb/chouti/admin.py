from django.contrib import admin

# Register your models here.
from .models import UserInfo, News, UserComment, UserRecommend, UserFavorite, ImageNews


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["username", "password", "email"]
    list_filter = ["username", "password", "email"]


class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "summary", "publisher", "href", "category", "recommend", "add_time"]
    list_filter = ["title", "publisher", "href", "category", "recommend"]


class UserCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "new", "content", "parent_id", "add_time"]
    list_filter = ["user", "new", "user", "content"]


class UserRecommendAdmin(admin.ModelAdmin):
    list_display = ["user", "new", "add_time"]
    list_filter = ["user", "new"]


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "new", "add_time"]
    list_filter = ["user", "new"]


class ImageNewsAdmin(admin.ModelAdmin):
    list_display = ["desc", "add_time"]


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(UserComment, UserCommentAdmin)
admin.site.register(UserRecommend, UserRecommendAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
admin.site.register(ImageNews, ImageNewsAdmin)