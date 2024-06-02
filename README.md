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

% py -m venv .venv

% .venv\Scripts\activate.bat

3.Djangoのインストール

(.venv)% py -m pip install Django

4.Djangoプロジェクトの作成

(.venv)% django-admin startproject config .

5.アプリの作成

(.venv)% py manage.py startapp booklog

■config/settings.py

6.モデルの作成と有効化

■booklog/models.py

(.venv)% py manage.py makemigrations

(.venv)% py manage.py migrate

7.管理ユーザーの作成

(.venv)% py manage.py createsuperuser

■booklog/admin.py

(.venv)% py manage.py runserver

http://127.0.0.1:8000/admin

8.アプリ処理、画面の作成

■config/urls.py

■booklog/views.py

■booklog/urls.py

■booklog/templates/booklog/*.html

9.アプリの確認

(.venv)% py manage.py runserver

http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
