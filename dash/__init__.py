import os

from flask import Flask, g, current_app, render_template, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required
from flask_mail import Mail
from flask_plugins import (
    PluginManager, get_enabled_plugins, get_plugin, Plugin, emit_event
)
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy


from dash.models import db, User, Role


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


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.init_app(app)
    db.app = app

    # hook up mail
    mail = Mail(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    with app.app_context():
        # Create admin
        if admin.app is None:
            admin.init_app(app)

        app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

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
