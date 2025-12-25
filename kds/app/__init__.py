from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


socketio = SocketIO(cors_allowed_origins="*")
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kds.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    socketio.init_app(app)


    from .routes import main
    app.register_blueprint(main)


    with app.app_context():
        db.create_all()


    return app
