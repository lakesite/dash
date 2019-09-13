import datetime

from flask_bcrypt import *
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


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
    notes = db.Column(db.Text, nullable=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    company_id = db.Column(db.Integer(), db.ForeignKey('company.id'))
    company = db.relationship('Company')

    def __unicode__(self):
        return("<User id={} email={}>".format(self.id, self.email))

    def __repr__(self):
        return("<User ID: {}, email: {}>".format(self.id, self.email))

    def __init__(self, email, password, roles, active=False, admin=False, confirmed_at=None):
        self.email = email
        self.password = password
        if admin:
            self.roles = [Role.query.filter_by(name='admin').first()]
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.active = active
        self.confirmed_at = confirmed_at

    def get_id(self):
        return self.id


class ServiceAgreement(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column('company_id', db.Integer(), db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company')
    name = db.Column(db.String(50), nullable=False)
    started_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    text = db.Column(db.Text, nullable=True, default='')

    def __unicode__(self):
        return("<started = %>".format(self.started_on))


class Company(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    bio = db.Column(db.String(255))
    users = db.relationship("User", backref="user", lazy="dynamic")

    def __repr__(self):
        return("{}".format(self.name))

    def __unicode__(self):
        return("<name = %>".format(self.name))


class UserRequest(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')
    requested_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    title = db.Column(db.String(255), nullable=False)
    request = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer)

    def __unicode__(self):
        return("<User=% request=%>".format(self.user.email, self.request))


class Iteration(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    project = db.Column('project_id', db.Integer(), db.ForeignKey('project.id'))


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column('company_id', db.Integer(), db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company')
    name = db.Column(db.String(255))
    status = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = tuple(db.UniqueConstraint('company', 'name', name='_company_projectname_uc'))

    def save_changes(self, form, new=False):
        self.name = form.name.data

        if new:
            db.session.add(project)

        db.session.commit()

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.name
