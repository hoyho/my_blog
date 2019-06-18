# Dday Blog

my personal blog
[here2say.tw](https://here2say.tw)

using Django with python 3.6
theme:google　Material design

Previously it host at [digital ocean](https://m.do.co/c/72dc886d7d8e)
but now migrated to Tencent Cloud for domestic visiting

### How to run on your local machine

1. prepare youe environment by running:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

2. then install dependences

    ``` bash
    pip install -r requirements.txt
    ```

3. set `DEBUG = True` in my_blog/settings.py

4. run server with port 8000

    ```bash
    python manage.py runserver
    ```

### Run in docker
1. build
`docker build -t here2say .`

2. run
`docker run  -d -p 8000:80 --name my_blog --restart=always  -v $(pwd)/media:/app/media here2say`

3. test it
`curl localhost:8000`

FAQ:

when update any css or js file
please remember to execute:
`python manage.py collectstatic`
and refresh browser page forcely

when change the field of model
run:

``` bash
python manage.py makemigrations
python manage.py migrate
```

### Deployment

1. update setting at my_blog/autostartwebsite.sh and my_blog/webconfig_uwsgi.ini
or
2. use docker ~~(still under development)~~

=======
**issue**

when editing the articles on admin panel please be careful to save markdown text
you need to paste markdown text to richtext box under source mod [see me](https://github.com/hoyho/my_blog/issues/34#issuecomment-459643028)
