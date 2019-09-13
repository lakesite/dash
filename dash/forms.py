import flask_login as login
from flask_wtf import Form
from wtforms import StringField, TextField
from wtforms.validators import InputRequired, DataRequired
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
from dash import db
from dash.models import Company, Project, UserRequest


class UserRequestForm(Form):

    request = TextField(validators=[InputRequired()], widget=TextArea())


class CompanyForm(Form):

    name = TextField(validators=[InputRequired()])
    email = EmailField('Main email address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    bio = TextField(validators=[InputRequired()])

    def validate_company(self, field):
        company = self.get_company()

        if company is None:
            raise validators.ValidationError('Invalid company')


    def get_company(self):
        return db.session.query(Company).filter_by(name=self.name.data).first()


class ProjectForm(Form):

    name = TextField(validators=[InputRequired()])

    def validate_project(self, field):
        project = self.get_project()

        if project is None:
            raise validators.ValidationError('Invalid project')


    def get_project(self):
        return db.session.query(Project).filter_by(name=self.name.data).first()
