
By default we use sqlite as our database

you can see related field at settings.py


```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

```


But now you can follow this instruction to migrate sqlite to mysql

1. create a database in mysql 
(I will assume to use the name `my_blog`,
Default Charset="utf8mb4"
Default Collation="utf8mb4_general_ci")

2. backup data from sqlite
`python manage.py dumpdata  --natural-foreign --natural-primary > datadump.json`

3. add mysql setting

open settings.py
update your info to the database part:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_blog', #databset name 
        'USER': 'user_name',
        'PASSWORD': 'you_psw',
        'HOST': 'somewhere.net',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

4. you need install mysql client and its dependeces

for macOS：

```bash
brew install mysql
pip install mysqlclient
```

for Linux:

`sudo apt-get install python3-dev # debian / Ubuntu`
or
`sudo yum install python3-devel # Red Hat / CentOS`

5. migrate the datestruct to new db
`python manage.py migrate`

6. import data to mysql

`python manage.py loaddata datadump.json`

done