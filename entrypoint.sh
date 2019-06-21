#!/bin/bash
python3 manage.py migrate                  # Apply database migrations
rm -rf collected_static && python3 manage.py collectstatic --noinput  # Collect static file

uwsgi --ini /app/my_blog/webconfig_uwsgi_docker.ini &

#EXPOSE 80
#CMD ["supervisord", "-n"]
nginx  -g "daemon off;"
