from flask import Flask, render_template, redirect, request, session, flash
from app.config import Config
from app.forms import OrderForm, LoginForm, RegisterForm
from app.user_function import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Dish, db.session))
admin.add_view(ModelView(Order, db.session))
# ------------------------------------------------------# Декораторы авторизации
# def login_required(f):
# (код декоратора)

# def admin_only(f):
# (код декоратора)


@app.route('/')
def render_main():
    diction = []
    # try:
    #     print(session['user'])
    # except:
    #     print('not user')
    '''
    for category_item in range(1, db.session.query(Category).count()+1):
        category_title = get_categories(category_item)
        diction.append({'title': category_title.title, 'dishes': list(get_dishes_for_category(category_item, 3))})

    return render_template("main.html", diction=diction)
    '''
    return "HI"


@app.route('/add_to_cart/', methods=['POST'])
def render_add_to_cart():
    add_to_cart(request.form.get('id'))
    # print('ADD_TO_CART', session['cart'])
    # return redirect('/cart/')
    return redirect('/')


@app.route('/delete_from_cart/', methods=['POST'])
def render_delete_from_cart():
    delete_from_cart(request.form.get('id'))
    # print('DEL_FROM_CART', session['cart'])
    flash('Блюдо было удалено')
    return redirect('/cart/')


@app.route('/cart/', methods=['GET', 'POST'])
def render_cart():
    form = OrderForm()
    # print('user= ', get_auth_user())
    if form.validate_on_submit():
        create_order(form)
        session['cart'] = empty_cart()
        return redirect('/ordered/')
    else:
        if request.method == 'GET' and session['user']:
            form.name.default = session['user'].get('name')
            form.email.default = session['user'].get('email')
            form.address.default = session['user'].get('address')
            # form.phone.default = session['user'].get('phone')
            form.process()
    # print(get_auth_user())
    # print(form.data)
    return render_template("cart.html", form=form, cart=get_cart())


@app.route('/account/', methods=['GET'])
def render_account():
    # session['cart'] = empty_cart()
    # print(get_auth_user())
    user = get_auth_user().get('id')
    orders = get_orders_by_user_id(user)
    # print(orders)
    return render_template("account.html", orders=orders)


@app.route('/auth/', methods=['GET', 'POST'])
def render_auth():
    form = LoginForm()
    # print('user= ', get_auth_user())
    if form.validate_on_submit():
        if login(form):
            return redirect('/account/')
        else:
            form.email.errors.append('Неверный пароль или email')
            return render_template('login.html', form=form)
    else:
        return render_template("login.html", form=form)


@app.route('/register/', methods=['GET', 'POST'])
def render_register():
    form = RegisterForm()
    if form.validate_on_submit():
        register(form)
        return redirect('/')
    else:
        return render_template("register.html", form=form)


@app.route('/logout/')
def render_logout():
    logout()
    empty_cart()
    return redirect('/auth/')


@app.route('/ordered/')
def render_ordered():
    return render_template("ordered.html")


if __name__ == "__main__":
    app.run()

# ------------------------------------------------------# Страница админки
# @app.route('/')@login_required def home():
# (код страницы админки)

# ------------------------------------------------------# Страница аутентификации
# @app.route("/login", methods=["GET", "POST"])def login():
# (код страницы аутентификации)

# ------------------------------------------------------# Страница выхода из админки
# @app.route('/logout', methods=["POST"])@login_required def logout():
# (код выхода из админки)

# ------------------------------------------------------# Страница добавления пользователя
# @app.route("/registration", methods=["GET", "POST"])@admin_only@login_required def registration():
# (код страницы регистрации)

# ------------------------------------------------------# Страница смены пароля
# @app.route("/change-password", methods=["GET", "POST"])@login_required def change_password():
# (код страницы смены пароля)
