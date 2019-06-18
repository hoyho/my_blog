#!/bin/bash
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static file

uwsgi --ini /app/my_blog/webconfig_uwsgi.ini &

#EXPOSE 80
#CMD ["supervisord", "-n"]
nginx  -g "daemon off;"
