# Elmer

Elmer is a social network inspired by [reddit](https://www.reddit.com/) built with [Python](https://www.python.org/) using the [Django Web Framework](https://www.djangoproject.com/).

### Demo

Check the website at [https://elmer.pythonanywhere.com](https://elmer.pythonanywhere.com/)

![Elmer Screenshot](https://image.ibb.co/eK4VBy/erebbit_screenshot.jpg "Elmer Screenshot")

### Technology Stack

* Python 3.6
* Django 1.8
* Django Rest Framework 3.3
* Twitter Bootstrap 4
* jQuery 3

### Installation Guide

Clone this repository:

```shell
$ git clone https://github.com/thetruefuss/elmer.git
```

Install requirements:

```shell
$ pip install -r requirements.txt
```

Copy `.env.example` file content to new `.env` file and update the credentials if any i.e Gmail account etc.

Run Django migrations to create database tables:

```shell
$ python manage.py migrate
```

Run the development server:

```shell
$ python manage.py runserver
```

Verify the deployment by navigating to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your preferred browser.
