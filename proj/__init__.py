from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from proj import config
from flask_cors import CORS
from proj.models import db

import os
def intial_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)
    app.config.from_object(config.config_setting[config_name])  # object-based default configuration
    app.config.from_pyfile('flask.cfg', silent=True)  # instance-folders configuration

    if config_name == 'production':
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = config.config_setting[config_name].SQLALCHEMY_ENGINE_OPTIONS
    db.init_app(app)

    from proj.views.external import bp_external
    app.register_blueprint(bp_external, url_prefix='/external')

    from proj.views.dev import bp_dev
    app.register_blueprint(bp_dev, url_prefix='/dev')

    from proj.views.user import bp_user
    app.register_blueprint(bp_user, url_prefix='/user')

    from proj.views.auth import bp_auth
    app.register_blueprint(bp_auth, url_prefix='/auth')

    from proj.views.lov import bp_lov
    app.register_blueprint(bp_lov, url_prefix='/lov')

    @app.route('/status', methods=['GET'])
    def new_api():
        return f'User Management OK'

    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app
