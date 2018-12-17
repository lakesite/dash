#!/usr/bin/env python

import datetime

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server, prompt, prompt_bool
from flask_migrate import Migrate, MigrateCommand

from dash import create_app, db
from dash.models import User, Project


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0", port=5000))


@manager.command
def drop_db():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def create_db(default_data=True, sample_data=False):
    "Creates database tables from sqlalchemy models"
    db.create_all()


@manager.command
def create_admin():
	"""Creates the admin user."""
	admin_login = prompt("Provide a login name")
	admin_email = prompt("Provide an email")
	admin_password = prompt("Provide a password")
	db.session.add(User(
		login=admin_login,
	    email=admin_email,
	    password=admin_password,
	    admin=True,
	    confirmed=True,
	    confirmed_on=datetime.datetime.now())
	)
	db.session.commit()


@manager.command
def create_user():
	"Creates a normal user"
	user_login = prompt("Provide a login name")
	user_email = prompt("Provide an email")
	user_password = prompt("Provide a password")
	db.session.add(User(
		login=user_login,
	    email=user_email,
	    password=user_password,
	    admin=False,
	    confirmed=False,
	))
	db.session.commit()


@manager.command
def create_project():
	"Creates a project"
	project_name = prompt("What name do you want for the project?")
	db.session.add(Project(
		name=project_name
	))
	db.session.commit()


if __name__ == "__main__":
	with app.app_context():
		db.init_app(current_app)
		db.app = current_app
		print("Using app instance: {} and db with engine: {}".format(current_app, db))

		manager.run()
