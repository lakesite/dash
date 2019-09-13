# dash #

A simple client dashboard and resource manager for technology focused businesses.  
Dash is the main base framework for managing customers clients, projects and
services.

Currently a draft with plugin layouts.

## Installing ##

    OSX/Linux:

    $ virtualenv -p python3 .env
    $ source .env/bin/activate
    $ (.env) pip install -r requirements.txt

## Running ##

If you're using vagrant, simply issue:

    $ vagrant up

If running locally and not using vagrant:

    $ source .env/bin/activate
    $ (.env) export FLASK_APP=dash
    $ (.env) export FLASK_ENV=development
    $ (.env) export APP_SETTINGS=dash.config.DevelopmentConfig
    $ (.env) flask run --host=0.0.0.0

    You can also issue:

    $ (.env) ./run.sh

    Or use manage.py:

    $ (.env) ./manage.py runserver

    Then view @ http://localhost:5000/
    admin user/pass: dash@lakesite.net / dash

## Dependencies ##

The following are primary dependencies, which are covered further in requirements.txt

    Flask
    Flask-Security
    Flask-Mail
    Flask-Admin
    Flask-Login
    Flask-Migrate
    Flask-Plugins
    Flask-SQLAlchemy
    Flask-WTF

## Migrations ##

Initialization, if for some reason the migrations folder does not exist;

    $ (.env) ./manage.py db init

Detect changes to db schema:

    $ (.env) ./manage.py db migrate

Apply migrations:

    $ (.env) ./manage.py db upgrade

## WIP ##

This is a work in progress and is not meant for production yet!

## License ##

MIT
