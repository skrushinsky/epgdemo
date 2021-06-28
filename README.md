# EPG demo

Демонстрация веб-сервиса по обработке фрагментов ТВ-расписаний. Фрагменты добываются из разных источников "веб-пауками".

- [EPG demo](#epg-demo)
  - [Платформа](#платформа)
  - [Начало работы](#начало-работы)
    - [Установка](#установка)
      - [Pip](#pip)
      - [Setuptools](#setuptools)
    - [Тестирование](#тестирование)
    - [Запуск](#запуск)
  - [Работа с сервисом](#работа-с-сервисом)
    - [Оглавление](#оглавление)
    - [Загрузка нового события](#загрузка-нового-события)
      - [Формат события](#формат-события)
    - [Журнал событий](#журнал-событий)

## Платформа

* Python >= 3.9
* Flask >= 2.0.1

Приложение тестировалась в среде **Ubuntu Linux 18.04**. Не должно возникать проблем и на других платформах,
совместимых с указанной версией Python-а. Все примеры ниже предполагают среду Linux с предустановленым **Python 3.9**.

## Начало работы

### Установка

Рекомендуется использовать [virtualenv](https://docs.python.org/3/library/venv.html) или аналогичный инструмент для того, чтобы програма работала в изолированном окружении.

```console
$ python3.9 -m venv ./venv
$ source ./venv/bin/activate
```

Установить сервис можно при помощи утилиты **pip** или **setuptools**. 

#### Pip

```console

(venv) $  pip install -r requirements.txt

```

#### Setuptools

```console

(venv) $ python setup.py install  

```

### Тестирование

```console

(venv) $ python -m unittest discover tests/

```

### Запуск

```console
(venv) $ export FLASK_APP=api.py
(venv) $ flask run

 * Serving Flask app 'api.py' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

Чтобы использовать другие опции запуска, см. [официальную документацию Flask](https://flask.palletsprojects.com/en/2.0.x/).

## Работа с сервисом

### Оглавление

Запрос по адресу `http://127.0.0.1:5000/` вернет JSON, где перчислены все доступные маршруты:

```console
(venv) $ curl --request GET --url http://127.0.0.1:5000/
```

```json
{
  "GET /": "Index page",
  "POST /service/hook": "Post new event"
}
```

### Загрузка нового события

Для создания нового события исользуется POST-запрос:

```console
(venv) $ curl --request POST \
              --url http://localhost:5000/service/hook \
              --header 'Content-Type: application/json' \
              --data EVENT'
```

#### Формат события

`EVENT` представляет собой JSON-структуру следующего содержания:

*  **jobid**: UID задания "паука", строка
*  **id_provider**: идентификатор провайдера,
*  **id_channel**: идентиыфикатор канала,
*  **week**: дата, с которой начинается неделя, формата `DD-MM-YYYY`,
*  **href**: адрес фрагмента расписания, URL-строка
*  **spider_name**: имя "паука", строка

Пример:

```json
{
  "jobid": "sdf4-dsfssd-sdfs-43fsdf",
  "id_provider": 1012,
  "id_channel": 2882,
  "week": "19-04-2021",
  "href": "https://storage.yandexcloud.net/epgtest/2021-04-12.json",
  "spider_name": "tt_ru"
}
```

### Журнал событий

Каждое событие, а также ошибки при попытке его получить, записывается в журнал **service.log**. Каждая запись представляет собой JSON. Пример:

```json
{
    "message": "success",
    "asctime": "2021-06-28 10:37:57",
    "event": {
        "jobid": "sdf4-dsfssd-sdfs-43fsdf",
        "id_provider": 1011,
        "id_channel": 2882,
        "week": "2022-04-19T00:00:00",
        "href": "https://storage.yandexcloud.net/epgtest/2882/2021-04-12.json",
        "spider_name": "tt_ru"
    }
}
{
    "message": "failure",
    "asctime": "2021-06-28 10:38:55",
    "error": "Key 'week' error:\nRegex('^(?:(?:0[1-9])|(?:[1,2][0-9])|(?:3[0-1]))-(?:(?:0[1-9])|(?:1[0-2]))-\\\\d{4}$') does not match 'aa-04-2022'"
}
```