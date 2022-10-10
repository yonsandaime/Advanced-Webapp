#Aanmaken centraal beheerde 'app' module waarbij alle bibliotheken worden geconfigureerd en opgestart.
#Aparte module vermijdt problemen rond circulair importeren

import flask, flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

login_manager = flask_login.LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = flask.Flask(__name__)
    app.secret_key = 'Change me! No, for real, change me!'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    
    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)    

    return app
