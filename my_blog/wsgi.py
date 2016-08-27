#!coding:utf-8
import os
from os.path import join,dirname,abspath

import sys
sys.path.append("/root/ENV3/lib/python3.5/site-packages")
 
PROJECT_DIR = dirname(dirname(abspath(__file__)))#3
import sys # 4
sys.path.insert(0,PROJECT_DIR) # 5

os.environ["DJANGO_SETTINGS_MODULE"] = "my_blog.settings" # 7
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
