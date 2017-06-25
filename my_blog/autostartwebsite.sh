#!/bin/sh
source /root/ENV35/bin/activate
pkill uwsgi
/root/ENV35/bin/uwsgi --ini /root/ENV35/bin/my_blog/my_blog/webconfig_uwsgi.ini --daemonize /var/log/uwsgi-emperor.log
