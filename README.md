# Erebbit

Erebbit is the follow-up of **[Rebbit](https://github.com/thetruefuss/rebbit/)** stating "Connecting people around the globe to help them share knowledge" built with [Python](https://www.python.org/) using the [Django Web Framework](https://www.djangoproject.com/).

**P.S:** Most of the **design flow** and **features** in this project are inspired by **[reddit](https://github.com/reddit-archive/reddit)**. It has a RESTful API which is implemented using [Django Rest Framework](http://django-rest-framework.org/).

### Demo

Check the website at [http://erebbit.pythonanywhere.com](http://erebbit.pythonanywhere.com/)

![Erebbit Screenshot](https://image.ibb.co/ddEd0T/erebbit_screenshot.jpg "Erebbit Screenshot")

### Technology Stack

* Python 3.6
* Django 1.8
* Django Rest Framework 3.3
* Twitter Bootstrap 4
* jQuery 3

### Installation Guide

Clone this repository:

```shell
$ git clone https://github.com/thetruefuss/erebbit.git
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
