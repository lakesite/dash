import datetime

from flask_bcrypt import *
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    active = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.String, nullable=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __unicode__(self):
        return("<User id=% email=%>".format(self.id, self.email))

    def __init__(self, email, password, roles, active=False, admin=False, confirmed_at=None):
        self.email = email
        self.password = password # generate_password_hash(password) #.decode('utf-8')
        self.roles = roles
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.active = active
        self.confirmed_at = confirmed_at

    def get_id(self):
        return self.id


users_projects = db.Table('users_projects',
    db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey("project.id"), primary_key=True),
)


# Create project model.
class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    users = db.relationship(User, secondary=users_projects, lazy='subquery', backref=db.backref('projects', lazy=True))

    def __init__(self, name, users=None):
        self.name = name

    def save_changes(self, form, new=False):
        self.name = form.name.data

        if new:
            db.session.add(project)

        db.session.commit()

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.name
