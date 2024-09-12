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
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sa-coma:Flask@mariadb/coma'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['SECRET_KEY'] = 'your-secret-key-for-sessions'
    
    # Initialisiere die Erweiterungen
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Importiere die Modelle nach der Initialisierung von db
    from app.models import User

    # Flask-Login User-Loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importiere Blueprints
    from app.routes import main
    from app.api import api
    from app.errors import errors
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(errors)
    
    return app
