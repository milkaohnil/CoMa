from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # MariaDB-Datenbank-Konfiguration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://<USERNAME>:<PASSWORD>@<SERVER>/<DATABASE>'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['SECRET_KEY'] = 'your-secret-key-for-sessions'
    
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from app.routes import main
    from app.api import api
    from app.errors import errors
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(errors)
    
    return app
