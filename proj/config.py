from urllib.parse import quote
import os
from sqlalchemy.engine import create_engine

class BaseConfig(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'  # changed to relative path
    TEMPLATE = 'static/template'  # changed to relative path
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    VERSION = ''

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 1,  # 🔑 at least 2
        "max_overflow": 0,  # 🔑 allow recovery
        "pool_recycle": 60,  # prevent silent close reuse
        "pool_pre_ping": True,
        "pool_timeout": 30
    }


class DevelopmentConfig(BaseConfig):
    # DB
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:%s@localhost:3306/user_management' % quote('c0008')
    DEBUG = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:%s@localhost:3306/flask_new_testing' % quote('s@m@dfans')
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Marlin2025")
    DB_SERVER = os.getenv("DB_SERVER", "127.0.0.1")
    DB_SCHEMA = os.getenv('DB_SCHEMA', "user_management")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:%s@{DB_SERVER}:3306/{DB_SCHEMA}' % quote(f'{DB_PASSWORD}')
    print("DB CONNECTION >>>>>>>>>>>> ", SQLALCHEMY_DATABASE_URI)



config_setting = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
