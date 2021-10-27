from flask import Flask
from app.config import Config
from app.models import db
from flask_migrate import Migrate
from app.models import Category, Dish, User, Order
from flask_wtf.csrf import CSRFProtect
import os


app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)
csrf.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


# Имортируем представление
from app.views import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
