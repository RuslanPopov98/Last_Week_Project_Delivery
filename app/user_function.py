import datetime
from flask import session
from sqlalchemy.sql.expression import func
from werkzeug.security import generate_password_hash, check_password_hash
import random
from app.models import db, Dish, Category, Order, User


def get_categories(category_id):
    return db.session.query(Category).filter(Category.id == category_id).first()


def get_dishes_for_category(category, count):
    return db.session.query(Dish).filter(Dish.category_id == category).order_by(func.random()).all()[:count]


def get_dish_by_id(dish_id):
    return db.session.query(Dish).get(int(dish_id))


def add_to_cart(dish_id):
    cart = get_cart()
    total = cart.get('total')
    qty = cart.get('qty')
    items = cart.get('items')
    dish = get_dish_by_id(dish_id)
    total += dish.price
    qty += 1
    if items.get(str(dish_id)) is None:
        items[dish_id] = {'title': dish.title, 'qty': 1, 'price': dish.price}
    else:
        items[dish_id]['title'] = dish.title
        items[dish_id]['qty'] += 1
        items[dish_id]['price'] += dish.price
    set_data_to_cart(qty, total, items)


def delete_from_cart(dish_id):
    cart = get_cart()
    total = cart.get('total')
    qty = cart.get('qty')
    items = cart.get('items')
    if items.get(str(dish_id)) is not None:
        item = items.get(dish_id)
        total -= item.get('price')
        qty -= 1
        items.pop(dish_id)
        set_data_to_cart(qty, total, items)


def set_data_to_cart(qty, total, items):
    qty_title = '{} {}'
    # .format(qty, plural_ru.ru(qty, ['блюдо', 'блюда', 'блюд']))
    session['cart'] = {'total': total, 'qty': qty, 'items': items, 'qty_title': qty_title}


def get_cart():
    if session.get('cart') is None:
        session['cart'] = {'total': 0, 'qty': 0, 'items': {}, 'qty_title': ''}
    return session['cart']


def empty_cart():
    return {'total': 0, 'qty': 0, 'items': {}, 'qty_title': ''}


def get_auth_user():
    if session.get('user'):
        return session['user']
    else:
        return None


def register(form):
    user = User()
    user.name = form.name.data
    user.email = form.email.data
    user.password = generate_password_hash(form.password.data)
    user.phone = form.phone.data
    user.address = form.address.data
    user.role = 'user'
    db.session.add(user)
    db.session.commit()


def logout():
    session.pop('user')


def login(form):
    user = db.session.query(User).filter(User.email == form.email.data).first()
    if user and check_password_hash(user.password, form.password.data):
        session['user'] = {'id': user.id, 'role': user.role, 'email': user.email, 'name': user.name,
                           'address': user.address, 'phone': user.phone}
        return True
    else:
        return False


def create_order(form):
    user = get_auth_user()
    order = Order()
    order.user_id = user.get('id')
    order.status = 'NEW'  # OrderStatus.NEW
    order.data = datetime.datetime.utcnow()
    form.populate_obj(order)

    cart = get_cart()
    order.total = cart.get('total')

    for item_id in cart['items']:
        meal = get_dish_by_id(int(item_id))
        order.dishes.append(meal)
    print(order.user, order.dishes)
    db.session.add(order)
    db.session.commit()

    empty_cart()


def get_orders_by_user_id(user_id):
    orders_data = []
    orders = db.session.query(Order).filter(Order.user_id == user_id).order_by(Order.data.desc()).all()

    for order in orders:
        order_item = {'total': order.total, 'status': order.status, 'date': order.data.date()}
        dishes_items = []
        for dish in order.dishes:
            dishes_items.append({'title': dish.title, 'qty': 1, 'price': dish.price})

        order_item['dishes'] = dishes_items
        orders_data.append(order_item)

    return orders_data
