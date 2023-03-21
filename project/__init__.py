import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager 
from flask_security import Security, SQLAlchemyUserDatastore
from dotenv import load_dotenv
load_dotenv()


db = SQLAlchemy()
from.models import User, Role
#creamos un objeto de sqlalchemyuserdatastore
userDataStore = SQLAlchemyUserDatastore(db, User, Role)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/flask_security'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = 'secretsalt'

    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()

    #Conectando los modelos de flask-security usando SQLALCHEMYUSERDATASTORE
    security = Security(app, userDataStore)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app