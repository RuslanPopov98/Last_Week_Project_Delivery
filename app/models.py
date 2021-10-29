from flask_sqlalchemy import SQLAlchemy
import enum
from werkzeug.security import generate_password_hash, check_password_hash

# Настройка соединения сделаем позже в модуле приложения
db = SQLAlchemy()


orders_meals_association = db.Table('orders_meals',
                db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
                db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id'))
                )


class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')
    orders = db.relationship("Order", secondary=orders_meals_association, back_populates='dishes')


class Category(db.Model):
    # __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    meals = db.relationship('Dish', back_populates='category')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(32), nullable=False)
    orders = db.relationship('Order', back_populates='user')


class OrderStatus(enum.Enum):
    NEW = 'Новый'
    PROCESSED = 'Выполняется'
    COMPLETED = 'Готово'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    dishes = db.relationship("Dish", secondary=orders_meals_association, back_populates='orders')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User')
