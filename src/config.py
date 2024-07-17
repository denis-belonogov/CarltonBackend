import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///carlton.db')


class DebugConfig(Config):
    DEBUG = True


class ReleaseConfig(Config):
    DEBUG = False


config_by_name = {
    'debug': DebugConfig,
    'release': ReleaseConfig,
    'default': ReleaseConfig
}
