# encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article
from datetime import datetime
import time
from django.http import Http404
import re
from django.contrib.syndication.views import Feed  #注意加入import语句
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  #添加分页包

# Create your views here.
def home(request):
    post_list = Article.objects.all() # 获取全部的Article对象
    for post in post_list:
        if post.intro:
            post.content=post.intro
        else:
            post.content = post.content[0:500]
                      
        if post.tags is not None:
            post.tags = str(post.tags).split(',')
    
    paginator = Paginator(post_list, 8) #每页显示10个
    page = request.GET.get('page')
    if page is None:
        page = 1

    try :
        post_list = paginator.page(page)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage :
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'post_list': post_list,'active_flag_home':'active'})


def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post' : post})







def archives(request) :
    try:
        post_list = Article.objects.order_by('-date_time')[:20]
    except Article.DoesNotExist :
        raise Http404
    return render(request, 'archives.html', {'post_list' : post_list,
                                            'error' : False,
                                            'active_flag_archive':'active'})



def about_me(request) :
    return render(request, 'aboutme.html',{'active_flag_aboutme':'active'})

def resume_zh(request) :
    return render(request, 'resume_zh.html')

def search_tag(request, tag) :
    try:
        post_list = Article.objects.filter(tags__contains=tag) #contains
        for post in post_list:
            if post.tags is not None:
                post.tags = str(post.tags).split(',')
    except Article.DoesNotExist :
        return render(request, 'tag.html',{})
        #raise Http404
    return render(request, 'tag.html', {'post_list' : post_list,
    'active_flag_tag':'active','tag_name':str(tag)})


def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request,'home.html')
        else:
            post_list = Article.objects.filter(title__icontains = s)
            if len(post_list) == 0 :
                return render(request,'search.html', {'post_list' : post_list,
                                                    'error' : True,
                                                    'active_flag_tag':'active'})
            else :
                return render(request,'search.html', {'post_list' : post_list,
                                                    'error' : False,
                                                    'active_flag_tag':'active'})
    return redirect('/')



class RSSFeed(Feed) :
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content

