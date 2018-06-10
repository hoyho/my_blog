"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
#from django.conf.urls import patterns, include, url
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.views.static import serve

from article.views import home,detail,weixin_main,archives,about_me,resume_zh,search_tag,blog_search,RSSFeed

from DjangoUeditor import urls as DjangoUeditor_urls
import  ckeditor

'''
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'article.views.home'),
    url(r'^(?P<id>\d+)/$', 'article.views.detail', name='detail'),
    url(r'^wechat', 'article.views.weixin_main'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    #url(r'^ueditor/', include('DjangoUeditor.urls' )),

)
'''
urlpatterns =[
    #'',
    # Examples:
    # url(r'^$', 'my_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^(?P<id>\d+)/$', detail, name='detail'),
    url(r'^archives/$', archives, name='archives'),
    url(r'^aboutme/$', about_me, name = 'about_me'),
    url(r'^resume_zh/$',resume_zh,name = 'resume_zh'),
    url(r'^tag/(?P<tag>\w+)/$', search_tag, name='search_tag'),
    url(r'^wechat', weixin_main,name='weixin_main'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^search/$',blog_search, name = 'search'),
    url(r'^feed/$', RSSFeed(), name="RSS"), #新添加的urlconf, 并将name设置为RSS, 方便在模板中使用url
    #url(r'^ueditor/', include('DjangoUeditor.urls' )),


]

# serving media files only on debug mode
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        })]
