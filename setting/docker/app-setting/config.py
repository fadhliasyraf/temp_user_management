import os
from urllib.parse import quote


class BaseConfig(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # check sql log
    SQLALCHEMY_POOL_SIZE = 50
    SQLALCHEMY_MAX_OVERFLOW = 80
    SECRET_KEY = 'secret'
    UPLOAD_FOLDER = 'static/uploads'  # changed to relative path
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 2,  # 🔑 at least 2
        "max_overflow": 1,  # 🔑 allow recovery
        "pool_recycle": 60,  # prevent silent close reuse
        "pool_pre_ping": True,
        "pool_timeout": 30
    }

class ProductionConfig(BaseConfig):
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Marlin2025")
    DB_SERVER = os.getenv("DB_SERVER", "127.0.0.1")
    DB_SCHEMA = os.getenv('DB_SCHEMA', "user_management")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:%s@{DB_SERVER}:3306/{DB_SCHEMA}' % quote(f'{DB_PASSWORD}')
    print("DB CONNECTION >>>>>>>>>>>> ", SQLALCHEMY_DATABASE_URI)


config_setting = {

    "production": ProductionConfig
}
