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

if you would like to use mysql please see docs/migrate2mysql.md


### Deployment

1. update setting at my_blog/autostartwebsite.sh and my_blog/webconfig_uwsgi.ini
or
2. use docker (still under development)


### Database

Previously, this project use SQLite as default database.
Using SQLite has some limitation. For exapmle, you need to copy and distribute the db file.
That's inconvenient and have some potential problem. That why I change to use MySQL by default.

fill you db info at settings.py or ststem Environment when you deploy or debug.

If you prefer to SQLite, see [docs](docs/sqlite.md). 
This should be fairly easy.

=======
**issue**

when editing the articles on admin panel please be careful to save markdown text
you need to paste markdown text to richtext box under source mod [see me](https://github.com/hoyho/my_blog/issues/34#issuecomment-459643028)
