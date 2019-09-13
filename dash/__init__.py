import os

from flask import Flask, g, current_app, render_template, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from flask_mail import Mail
from flask_plugins import (
    PluginManager, get_enabled_plugins, get_plugin, Plugin, emit_event
)
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields import PasswordField

from dash.models import (
    db, User, UserRequest, Role, Company, Project, ServiceAgreement
)
from dash.blueprints import (
    user_bp, company_bp, request_bp, project_bp
)


def create_admin(app=None, *args, **kwargs):
    return Admin(app, *args, **kwargs)


admin = create_admin()


def _get_bool_env_var(varname, default=None):
    value = os.environ.get(varname, default)

    if value is None:
        return False
    elif isinstance(value, str) and value.lower() == 'false':
        return False
    elif bool(value) is False:
        return False
    else:
        return bool(value)


class AppPlugin(Plugin):

    def register_blueprint(self, blueprint, **kwargs):
        current_app.register_blueprint(blueprint, **kwargs)

    def register_admin(self, models, **kwargs):
        for model in models:
            admin.add_view(ModelView(model, db.session))

# Create a user and role admin interface to restrict access
# to flask_admin

class BaseAdmin(ModelView):

    def is_accessible(self):
        return current_user.has_role('admin')


class UserAdmin(ModelView):

    column_exclude_list = list = ('password',)
    form_excluded_columns = ('password',)
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):

        if len(model.password2):
            model.password = utils.encrypt_password(model.password2)


class RoleAdmin(ModelView):

    def is_accessible(self):
        return current_user.has_role('admin')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    db.app = app

    # hook up mail
    mail = Mail(app)

    try:
        # initialize data store and setup roles, security
        # this will fail if the db does not exist ...
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='client', description='Client')
        user_datastore.commit()
        security = Security(app, user_datastore)
    except:
        pass

    with app.app_context():
        # Create admin
        if admin.app is None:
            admin.init_app(app)

        app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(RoleAdmin(Role, db.session))
        admin.add_view(BaseAdmin(Company, db.session))
        admin.add_view(BaseAdmin(UserRequest, db.session))
        admin.add_view(BaseAdmin(Project, db.session))
        admin.add_view(BaseAdmin(ServiceAgreement, db.session))

        # Initialize the plugin manager
        plugin_manager = PluginManager(app)
        plugins = get_enabled_plugins()

        if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
        else:
            # load the test config if passed in
            app.config.from_mapping(test_config)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        app.register_blueprint(user_bp)
        app.register_blueprint(company_bp)
        app.register_blueprint(request_bp)
        app.register_blueprint(project_bp)

        # internal version
        @app.route('/version')
        def version():
            return app_version

        # index
        @app.route("/")
        def index():
            return render_template("index.html")

        @app.route("/plugins")
        @login_required
        def plugins():
            return render_template("plugins.html", plugins=get_enabled_plugins())

        @app.route("/disable/<plugin>")
        def disable(plugin):
            plugin = get_plugin(plugin)
            plugin_manager.disable_plugins([plugin])
            return redirect(url_for("index"))

        @app.route("/enable/<plugin>")
        def enable(plugin):
            plugin = get_plugin(plugin)
            plugin_manager.enable_plugins([plugin])
            return redirect(url_for("index"))

    return app
