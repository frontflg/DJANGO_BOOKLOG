参考サイト

　https://qiita.com/wawana12/items/7efad3908c3535fe1ac7#booklog%E3%81%AE%E5%89%8A%E9%99%A4

　　Djangoで読書メモアプリを作る

　https://tech-diary.net/django-todo-tutorial/#index_id0

　　【Django入門】初心者でも1時間でWebアプリ（Todoアプリ）を作成するコース

実行環境：Windows 10 Home 22H2
　　using Django 5.0.6.

1.Pythonのインストール（既存の場合は不要）

　https://www.python.org/downloads/

　python-3.12.3-amd64.exe

2.仮想環境の構築

コマンドプロンプトから

　% mkdir django-booklog

　% cd django-booklog

　% py -m venv myvenv

　% myvenv\Scripts\activate.bat

3.Djangoのインストール

　(myvenv)% py -m pip install Django

4.Djangoプロジェクトの作成

　(myvenv)% django-admin startproject mysite .

5.アプリの作成

　(myvenv)% py manage.py startapp app

　■mysite/settings.py

　必要であれば

　　(myvenv)% pip install django-widget-tweaks

　　(myvenv)% pip install django-accounts

　　(myvenv)% pip install django-allauth

　　(myvenv)% pip install requests

　　等

6.モデルの作成と有効化

　■app/models.py

　(myvenv)% py manage.py makemigrations

　(myvenv)% py manage.py migrate

7.管理ユーザーの作成

　(myvenv)% py manage.py createsuperuser

　■app/admin.py

　(myvenv)% py manage.py runserver

　http://127.0.0.1:8000/admin

8.アプリ処理、画面の作成

　■mysite/urls.py

　■app/views.py

　■app/forms.py

　■app/urls.py

　■app/templates/app/*.html

9.アプリの確認

　(myvenv)% py manage.py runserver

　http://127.0.0.1:8000/

　Quit the server with CTRL-BREAK.
