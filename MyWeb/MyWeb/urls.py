"""MyWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from chouti.views import IndexView, RegisterView, LoginView, LogoutView, RecommendView, AjaxUploadImageView, IdentifyCodeView, UserCommentView, UploadImageView, ArticleView
from django.views.static import serve
from .settings import MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^recommend/$', RecommendView.as_view(), name="recommend"),
    url(r'^ajax_upload_image/$', AjaxUploadImageView.as_view(), name="ajax_upload_image"),
    url(r'^identify_code/$', IdentifyCodeView.as_view(), name="identify_code"),
    url(r'^user_comment/(?P<news_id>\d+)/$', UserCommentView.as_view(), name="user_comment"),
    url(r'^upload_image/$', UploadImageView.as_view(), name="upload_image"),
    url(r'^article/$', ArticleView.as_view(), name="article"),
]
