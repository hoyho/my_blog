#!/bin/sh
source /home/ubuntu/env35/bin/activate
pkill uwsgi
/home/ubuntu/env35/bin/uwsgi --ini /home/ubuntu/my_blog/my_blog/webconfig_uwsgi.ini --daemonize /var/log/uwsgi-emperor.log
