#coding:utf-8
from django.db import models
from django.core.urlresolvers import reverse

#see how to add editor http://www.ziqiangxuetang.com/django/django-cms-develop2.html'
from DjangoUeditor.models import UEditorField
from ckeditor.fields import RichTextField


# Create your models here.
class Article(models.Model) :
    title = models.CharField(max_length = 100)  #博客题目
    category = models.CharField(max_length = 50, blank = True)  #博客标签
    intro = models.TextField(max_length=500,null = True,blank=True)
    date_time = models.DateTimeField(auto_now_add = True)  #博客日期
    #content = models.TextField(blank = True, null = True)  #博客文章正文
    content = RichTextField('正文')
    '''
    content = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    '''
    #python2使用__unicode__, python3使用__str__
    def __str__(self) :
        return self.title


#获取URL并转换成url的表示格式
    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id':self.id})
        return "http://hear2say.me%s" % path


    class Meta:  #按时间下降排序
        ordering = ['-date_time']
