from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Настройка соединения сделаем позже в модуле приложения
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    about = db.Column(db.String)
    rating = db.Column(db.Float)
    picture = db.Column(db.String)
    price = db.Column(db.Integer)
    goals = db.Column(db.JSON)
    free = db.Column(db.JSON)