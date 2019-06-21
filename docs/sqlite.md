sicne now Dday blog is using mysql by default

see migrate2mysql.md for context

However, you can still use sqlite as storage backend

go to settings.py

you can see related congiguration , enable it

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

```

also remember to disable previous setting.

You may need to apply maigration (optional)

```python
python manage.py makemigrations
python manage.py migrate
```