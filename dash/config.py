# Taken from:
# https://github.com/realpython/flask-registration/blob/master/project/config.py

import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))


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


class BaseConfig(object):
    """Base configuration."""

    # main config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'notsecret')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'notsecret2')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail settings
    MAIL_SERVER = os.environ.get('APP_MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('APP_MAIL_PORT', 465))
    MAIL_USE_TLS = _get_bool_env_var('APP_MAIL_USE_TLS', False)
    MAIL_USE_SSL = _get_bool_env_var('APP_MAIL_USE_SSL', True)

    # mail authentication
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME', None) # None
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD', None) # None

    # mail accounts
    MAIL_DEFAULT_SENDER = 'hello@lakesite.net'
    # https://github.com/mattupstate/flask-security/issues/685
    SECURITY_EMAIL_SENDER = MAIL_DEFAULT_SENDER

    # security settings
    SECURITY_URL_PREFIX = '/auth'
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True

    EXPLAIN_TEMPLATE_LOADING = True

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dash:dash@localhost/dash'
    #'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    DEBUG_TB_ENABLED = True

    # The development config takes precedence over env variables
    # development config file at ./project/config/development.cfg
    config_path = os.path.join(basedir, 'config', 'development.cfg')

    # if config file exists, read it:
    if os.path.isfile(config_path):
        config = configparser.ConfigParser()

        with open(config_path) as configfile:
            config.readfp(configfile)

        SECRET_KEY = config.get('keys', 'SECRET_KEY')
        SECURITY_PASSWORD_SALT = config.get('keys', 'SECRET_KEY')

        # mail settings
        MAIL_SERVER = config.get('mail', 'MAIL_SERVER')
        MAIL_PORT = config.getint('mail', 'MAIL_PORT')
        MAIL_USE_TLS = config.getboolean('mail', 'MAIL_USE_TLS')
        MAIL_USE_SSL = config.getboolean('mail', 'MAIL_USE_SSL')

        # mail authentication and sender
        MAIL_USERNAME = config.get('mail', 'MAIL_USERNAME')
        MAIL_PASSWORD = config.get('mail', 'MAIL_PASSWORD')
        MAIL_DEFAULT_SENDER = config.get('mail', 'MAIL_DEFAULT_SENDER')
        SECURITY_EMAIL_SENDER = MAIL_DEFAULT_SENDER

        # database URI
        SQLALCHEMY_DATABASE_URI = config.get('db', 'SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    """Testing configuration."""
    LOGIN_DISABLED=False
    TESTING = True
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    DEBUG_TB_ENABLED = False

    SECRET_KEY = None
    SECURITY_PASSWORD_SALT = None

    SQLALCHEMY_DATABASE_URI = None

    # The production config takes precedence over env variables
    # production config file at ./project/config/production.cfg
    config_path = os.path.join(basedir, 'config', 'production.cfg')

    # if config file exists, read it:
    if os.path.isfile(config_path):
        config = configparser.ConfigParser()

        with open(config_path) as configfile:
            config.readfp(configfile)

        SECRET_KEY = config.get('keys', 'SECRET_KEY')
        SECURITY_PASSWORD_SALT = config.get('keys', 'SECRET_KEY')

        # mail settings
        MAIL_SERVER = config.get('mail', 'MAIL_SERVER')
        MAIL_PORT = config.getint('mail', 'MAIL_PORT')
        MAIL_USE_TLS = config.getboolean('mail', 'MAIL_USE_TLS')
        MAIL_USE_SSL = config.getboolean('mail', 'MAIL_USE_SSL')

        # mail authentication and sender
        MAIL_USERNAME = config.get('mail', 'MAIL_USERNAME')
        MAIL_PASSWORD = config.get('mail', 'MAIL_PASSWORD')
        MAIL_DEFAULT_SENDER = config.get('mail', 'MAIL_DEFAULT_SENDER')
        SECURITY_EMAIL_SENDER = MAIL_DEFAULT_SENDER

        # database URI
        SQLALCHEMY_DATABASE_URI = config.get('db', 'SQLALCHEMY_DATABASE_URI')
