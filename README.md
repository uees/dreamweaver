# Dreamweaver

关于朋友的朋友的一个梦想

### 安装

python >= 3.6

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/sar.json
```

### 启动服务器

```
python manage.py runserver
```


### 升级

date: 2019-03-18

```
python manage.py makemigrations
python manage.py migrate
python manage.py seed_options
```