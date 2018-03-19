# encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article
from datetime import datetime
import time
from django.http import Http404
import re
from django.contrib.syndication.views import Feed  #注意加入import语句

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

    return render(request, 'home.html', {'post_list': post_list,'active_flag_home':'active'})


def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post' : post})







def archives(request) :
    try:
        post_list = Article.objects.all()[：20]
    except Article.DoesNotExist :
        raise Http404
    return render(request, 'archives.html', {'post_list' : post_list,
                                            'error' : False,
                                            'active_flag_archive':'active'})



def about_me(request) :
    return render(request, 'aboutme.html',{'active_flag_aboutme':'active'})



def search_tag(request, tag) :
    try:
        post_list = Article.objects.filter(category__iexact = tag) #contains
    except Article.DoesNotExist :
        raise Http404
    return render(request, 'tag.html', {'post_list' : post_list,
    'active_flag_tag':'active'})


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


# wechat here

import sys

sys.path.append("/root/ENV3/lib/python3.5/site-packages")

import hashlib
import json
from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# from auto_reply.views import auto_reply_main # 修改这里
from django.core.mail import send_mail, EmailMultiAlternatives
import xml.etree.ElementTree

WEIXIN_TOKEN = 'hoyho'

global MSGID
MSGID=0


imgresult={}


@csrf_exempt
def weixin_main(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    global MSGID
    global imgresult
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = tmp_str.encode('utf-8')
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    else:
        fi = open("/tmp/req.txt", "wb")
        fi.write(request.body)
        fi.close()
        content = str(request.body, 'utf-8')#content is a string of a xml file
        msg = parse_msg(content) #msg is a dict
        if msg['MsgType']=='event':
            msg["MsgId"]=int(time.time())
        # send_mail(u'Wechat Debug',' in image proceding1', 'rome1qaz@163.com', ['rome2wsx@163.com'], fail_silently=False)
        if MSGID ==msg["MsgId"]: #if 5s repeat mesage
            print('\n\n\n'+'result'+str(imgresult))
            if str(MSGID) in imgresult:
                response = response_msg(imgresult[MSGID], "image")
                print("fuck your tencent,you should waiting ")
                return HttpResponse(response)
        else:
            MSGID=msg["MsgId"]
            if msg["MsgType"] == "image":
                #return HttpResponse("")  # 长时间处理
                send_mail(u'Wechat Debug', 'msg[picurl]=s\n in if msg["msgType"]=="image"', 'rome1qaz@163.com',
                          ['rome2wsx@163.com'], fail_silently=False)
                msg["Content"] = gettag(msg["PicUrl"])
                imgresult[str(MSGID)] = msg
                print('MSGID:'+str(MSGID)+'\n')
                print('\n\n\n'+'msg:'+ str(msg))
                send_mail(u'Wechat Debug', msg["Content"], 'rome1qaz@163.com', ['rome2wsx@163.com'],
                          fail_silently=False)
                response = response_msg(msg, "image")
                return HttpResponse(response)
            elif msg["MsgType"] == "text":
                response = response_msg(msg, "text")
                return HttpResponse(response)
            elif msg["MsgType"] =="event":
                response = response_msg(msg,"event")
                return HttpResponse(response)


            # response = response_msg(msg,messagetype)
        # msg = str(msg,'utf-8')
        # mail(request.body)
        send_mail(u'Wechat Debug', 'content:\n' + content, 'rome1qaz@163.com', ['rome2wsx@163.com'],
                  fail_silently=False)
        xml_str = smart_str(request.body)
        request_xml = etree.fromstring(xml_str)
        #return HttpResponse(response)


def mail(content):
    subject, from_email, to = 'Wechat Debug', 'rome1qaz@163.com', 'rome2wsx@163.com'
    text_content = 'This is the debug message.'
    text_content = text_content  # +'\n'+content+"\n"
    # html_content = '<p>This is an <strong>important</strong> message.</p>'
    html_content = str(request.body, 'utf-8')
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def parse_msg(recvmsg):
    """
    这里是用来解析微信Server Post过来的XML数据的，取出各字段对应的值，以备后面的代码调用，也可用lxml等模块。
    """
    recvmsg  # request.body.read()
    ET = xml.etree.ElementTree
    root = ET.fromstring(recvmsg)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg


def response_msg(re_msg, messageType):
    """
    这里是响应微信Server的请求，并返回数据的主函数，判断Content内容
    基本思路：
    # 拿到Post过来的数据
    # 分析数据（拿到FromUserName、ToUserName、CreateTime、MsgType和content）
    # 构造回复信息（将你组织好的content返回给用户）
    """
    # 拿到并解析数据
    msg = re_msg
    # 设置返回数据模板
    # 纯文本格式
    textTpl = """<xml>
             <ToUserName><![CDATA[%s]]></ToUserName>
             <FromUserName><![CDATA[%s]]></FromUserName>
             <CreateTime>%s</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[%s]]></Content>
             <esponse(response)Flag>
             </xml>"""
    if messageType == 'text':
        echostr = textTpl % (
            msg['FromUserName'],
            msg['ToUserName'],
            str(int(time.time())),
            u"你是说：" + msg['Content'])
    elif messageType == 'image':
        echostr = textTpl % (
            msg['FromUserName'],
            msg['ToUserName'],
            str(int(time.time())),
            u"老夫掐指一算，这图应有：\n" + msg['Content'])
    elif messageType == 'default':
        echostr = textTpl % (
            msg['FromUserName'],
            msg['ToUserName'],
            str(int(time.time())),
            u"客官请稍等，正在处理啦")
    elif messageType =='event':
        echostr = textTpl % (
            msg['FromUserName'],
            msg['ToUserName'],
            str(int(time.time())),
            u"哟哟客官，像你这么有眼光的人不多咯～")
    return echostr


import http.client, urllib.request, urllib.parse, urllib.error, base64
import xml.etree.ElementTree
import json


def gettag(url):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '3c87f5c0cace407180d136bef01eb560'
    }

    class JSONObject:

        def __init__(self, d):
            self.__dict__ = d

    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/vision/v1.0/tag",
                 "{'url':'%s'}" % url,
                 headers)
    try:
        response = conn.getresponse()
        data = response.read()
        conn.close()
        resp = json.loads(str(data, 'utf-8'))
        data = json.loads(str(data, 'utf-8'), object_hook=JSONObject)
        result = ""
        for e in data.tags:
            result = result + e.name + " , " + "reliability:" + str(int(e.confidence * 100)) + "%" + "\n"
            # print(e.name +" , " + "reliability:"+ str(int(e.confidence*100)) +"%")
        print("-----result-data----\n")
        print(result)
    except Exception as e:
        result = e.__str__()
    finally:
        if not result:
            print("咦没有结果哦，服务好像挂了惹。。")
            result = "咦没有结果哦，服务好像挂了惹。。 "
        return result

    print(result)


