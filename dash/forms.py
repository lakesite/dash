import flask_login as login
from flask_wtf import Form
from wtforms import StringField, TextField
from wtforms.validators import InputRequired, DataRequired
from dash import db
from dash.models import Project


class ProjectForm(Form):

    name = TextField(validators=[InputRequired()])

    def validate_project(self, field):
        project = self.get_project()

        if project is None:
            raise validators.ValidationError('Invalid project')


    def get_project(self):
        return db.session.query(Project).filter_by(name=self.name.data).first()
