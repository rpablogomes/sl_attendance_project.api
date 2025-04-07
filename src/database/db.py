from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src import bcrypt

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)