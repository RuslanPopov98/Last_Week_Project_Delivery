from app.models import Category, Dish
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Config
from app.models import db
from app import app
import csv

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

categories_data = csv.DictReader(open('categories.csv'), delimiter=";")
meals_data = csv.DictReader(open('meals.csv'), delimiter=";")

with app.app_context():
    db.create_all()


for category_item in categories_data:
    session.add(Category(id=category_item.get('id'), title=category_item.get('title')))

session.commit()


for meals_item in meals_data:
    session.add(Dish(id=meals_item.get('id'), title=meals_item.get('title'), price=meals_item.get('price'),
                     description=meals_item.get('description'), picture=meals_item.get('picture'),
                     category_id=meals_item.get('category_id')))

session.commit()


# print(db.session.query(Dish).filter(Dish.id == 1).first())
