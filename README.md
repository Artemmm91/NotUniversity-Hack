# NotUniversity-Hack

Наш проект к хакатону. Я пока начну делать шаблон сайта и когда закончу напишу как его запускать у себя


Что нужно для запуска проекта
-------------

- Установите все необходимые пакеты:
Если у вас Линукс:
```
sudo apt-get install git
sudo apt-get install python3-virtualenv virtualenv  
```
VirtualEnv можно скачать и через pip, а git через сайт
```
pip install virtualenv
```

- Склонируйте проект с GitHub
- Создайте и запустите отдельное виртуальное окружение(указывать собственную папку расположения питона):
```
mkdir ~/venvs
cd ~/venvs
virtualenv -p /usr/bin/python3 mlh_hack_env
source ~/venvs/dj_venv/bin/activate
```
Или создайте автоматически в PyCharm
- Перейдите в папку проекта (предположим, что она находится прямо в домашней): 
```
cd ~/NotUnoversity-Hack
```
- Установите все необходимые пакеты: 
```
pip install -r mlh/requirements.txt
```
- Запустите процесс инициализации БД: 
```
python mlh/manage.py makemigrations
python mlh/manage.py migrate
```

- Настройте проект в PyCharm:
  - File->New project
  - Путь к папке проекта: ~/NotUnoversity-Hack
  - Интерпретатор: Add local -> Выбираем "~/venvs/mlh_hack_env/bin/python3" -> Ok -> Ждём, пока окружение проиндексируется
  - Нажимаем Ok и соглашаемся с предложением создать проект из существующих исходников
  - Добавляем конфигурацию запуска: "Edit configurations" -> "+" - > Python -> Имя скрипта: mlh/manage.py -> параметр "runserver" -> Apply -> Ok
- Проект готов к запуску.
