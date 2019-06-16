uwsgi --ini /app/my_blog/webconfig_uwsgi.ini &

#EXPOSE 80
#CMD ["supervisord", "-n"]
nginx  -g "daemon off;"
