1. Клонируем репозиторий:

```sh
git clone https://github.com/Korabnick/rpm_flask_project.git
```

2. Для корректной работы приложения требуется установить python3.10 с дистрибутивами:

```sh
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-dev python3.10-venv python3.10-distutils python3.10-lib2to3 python3.10-gdbm python3.10-tk
```

3. В склонированном репозитории создаём виртуальную среду на python3.10:

```sh
python3.10 -m venv ./venv
```
И сразу запускаем ёё

```sh
. ./venv/bin/activate
```

4. Далее потребуется создать докер с базой данных:

```sh
docker run  -d \
        --name flask_proj \
        -e POSTGRES_USER=fladmin \
        -e POSTGRES_PASSWORD=test \
        -e PGDATA=/postgres_data_inside_container \
        -v ~/flask_project/postgres_data:/postgres_data_inside_container \
        -p 38764:5432 \
        postgres:15.1
```

5. И саму базу данных в докере:

```sh
1. docker exec -it flask_proj psql -U fladmin

2. CREATE DATABASE flask_db;
```

6. Устанавливаем нужные библиотеки:

```sh
pip install flask flask-sqlalchemy flask-login flask-mail python-dotenv pyscopg2-binary flask-wtf validate_email_address flask_admin alembic
```

7. Прописываем команду для применения миграций:

```sh
alembic upgrade head
```

8. После создания базы данных и миграций запускаем по очереди скрипты, которые находятся в репозитории с названиями:

```
1_scriptforroles.py и 2_scriptforadmin.py
```

9. В папке /app/ создайте .env файл в котором пропишите:

```
SECRET_KEY=yourkey
DATABASE_URL=postgresql://fladmin:test@localhost:38764/flask_db
USER_MAIL=yourmail
PASS_MAIL=yourapppasswordmail
```
10. Теперь можно запустить сайт запустив python файл run.py
