# Elmer

[![Build Status](https://travis-ci.org/thetruefuss/elmer.svg?branch=master)](https://travis-ci.org/thetruefuss/elmer)
[![Coverage Status](https://coveralls.io/repos/github/thetruefuss/elmer/badge.svg?branch=master)](https://coveralls.io/github/thetruefuss/elmer?branch=master)
[![Requirements Status](https://requires.io/github/thetruefuss/elmer/requirements.svg?branch=master)](https://requires.io/github/thetruefuss/elmer/requirements/?branch=master)

Elmer is a social network inspired by [reddit](https://www.reddit.com/) built with [Python](https://www.python.org/) using the [Django Web Framework](https://www.djangoproject.com/).

### Demo

Check the website at [https://elmer.pythonanywhere.com](https://elmer.pythonanywhere.com/)

![Elmer Screenshot](https://image.ibb.co/es9ymz/elmer_screenshot.jpg "Elmer Screenshot")

### Technology Stack

* [Python](https://www.python.org/) 3.6.x
* [Django Web Framework](https://www.djangoproject.com/) 2.1.x
* [Django Rest Framework](http://www.django-rest-framework.org/) 3.8.x
* [Twitter Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
* [jQuery 3](https://api.jquery.com/)

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

Load initial data for flatpages from fixtures folder:

```shell
$ python manage.py loaddata fixtures/flatpages_data.json
```

[Optional] Populate the database with dummy data:

```shell
$ python scripts/populate_database.py
```

Run the development server:

```shell
$ python manage.py runserver
```

Verify the deployment by navigating to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your preferred browser.
