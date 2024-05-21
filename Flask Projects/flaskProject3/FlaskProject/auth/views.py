from . import auth
from .forms import LogForm, RegForm, LogOut, AddToCart, RemoveFromCart, AddProduct
from flask import request, render_template, url_for, redirect
from flask_mail import Message
from threading import Thread
from FlaskProject.models import User, Item, Type, cart_items
from FlaskProject import mail, db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import text
from FlaskProject.decorators import permission_required
from flask_admin.contrib.sqla import ModelView


# Landing page with accessible actions:
# Login: Modal window where only existing accounts can be entered
# Register: Modal window where only non-existing accounts can be created
# Logout: Modal window where an authorized user can exit from their account
@auth.route("/", methods=['GET', 'POST'])
def landing():
    logForm = LogForm(prefix="logForm")
    regForm = RegForm(prefix="regForm")
    logout = LogOut(prefix="logout")
    items = Item.query.all()
    types = Type.query.all()

    if regForm.validate_on_submit() and regForm.submitReg.data:
        if User.query.filter_by(email=regForm.emailVal.data).first():
            return redirect(url_for('auth.landing'))
        new_user = User(email=regForm.emailVal.data)
        new_user.set_password(regForm.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_conf_token()
        send_confirm(new_user, token)
        login_user(new_user)
        return render_template('auth/follow_email.html')

    if logForm.validate_on_submit() and logForm.submitIn.data:
        user = User.query.filter_by(email=logForm.emailVal.data).first()
        if user is not None and user.password_verify(logForm.password.data):
            login_user(user)
            return redirect(url_for('auth.landing'))

    if logout.validate_on_submit() and logout.submitOut.data:
        logout_user()
        return redirect(url_for('auth.landing'))

    return render_template('pages/landing.html', logform=logForm, regform=regForm, logout=logout,
                           items=items, types=types)


# Cart page, which is only accessible to Users and higher. Accessible actions:
# Remove From Cart: Each individual item can be removed by submitting "Remove" field
# If user's cart contains at least one item, then a card with item name, price and remove item button will appear.
# Also total price will appear under the item cards
# If user's cart is empty, then a certain message will appear with a link to catalog
@auth.route("/cart", methods=['GET', 'POST'])
@permission_required(1)
def cart():
    remove = RemoveFromCart(prefix="remove")
    logout = LogOut(prefix="logout")
    temp_cart = db.session.query(cart_items).filter_by(user_id=current_user.id).all()
    user_cart = []
    total = 0
    for i in temp_cart:
        user_cart.append(Item.query.filter_by(id=i[1]).first())
        total += user_cart[-1].price

    if remove.validate_on_submit() and remove.submitRem.data:
        item_id = request.form.get('item_id')
        user_id = current_user.id
        sql_query = text(
            "DELETE FROM cart_items WHERE user_id = :user_id AND item_id = :item_id LIMIT 1"
        )
        db.session.execute(sql_query, {'user_id': user_id, 'item_id': item_id})
        db.session.commit()
        temp_cart = db.session.query(cart_items).filter_by(user_id=current_user.id).all()
        user_cart = []
        total = 0
        for i in temp_cart:
            user_cart.append(Item.query.filter_by(id=i[1]).first())
            total += user_cart[-1].price

        return redirect(url_for('auth.cart'))

    if logout.validate_on_submit() and logout.submitOut.data:
        logout_user()
        return redirect(url_for('auth.landing'))

    return render_template('pages/cart.html', remove=remove, logout=logout, user_cart=user_cart, total=total)


# A code that stands for 6 different pages. They share similar function, so they are
# united by one code and one html document
# Accessible actions:
# Login, Register, Logout
# Pages with basic info, such as working hours and pick-up sites
@auth.route("/about", methods=['GET', 'POST'])
@auth.route("/pickup", methods=['GET', 'POST'])
@auth.route("/shipping", methods=['GET', 'POST'])
@auth.route("/hours", methods=['GET', 'POST'])
@auth.route("/policy", methods=['GET', 'POST'])
@auth.route("/design", methods=['GET', 'POST'])
def cart_manage():
    logForm = LogForm(prefix="logForm")
    regForm = RegForm(prefix="regForm")
    logout = LogOut(prefix="logout")
    types = Type.query.all()

    if regForm.validate_on_submit() and regForm.submitReg.data:
        if User.query.filter_by(email=regForm.emailVal.data).first():
            return redirect(url_for('auth.landing'))
        new_user = User(email=regForm.emailVal.data)
        new_user.set_password(regForm.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_conf_token()
        send_confirm(new_user, token)
        login_user(new_user)
        return render_template('auth/follow_email.html')

    if logForm.validate_on_submit() and logForm.submitIn.data:
        user = User.query.filter_by(email=logForm.emailVal.data).first()
        if user is not None and user.password_verify(logForm.password.data):
            login_user(user)
            return render_template('pages/multi_use.html', logform=logForm, regform=regForm, logout=logout, types=types,
                                   req_path=request.path)

    if logout.validate_on_submit() and logout.submitOut.data:
        logout_user()
        return render_template('pages/multi_use.html', logform=logForm, regform=regForm, logout=logout, types=types,
                               req_path=request.path)

    return render_template('pages/multi_use.html', logform=logForm, regform=regForm, logout=logout, types=types,
                           req_path=request.path)


# Catalog page. Can be delivered by two ways:
# 1. By simply going to catalog
# 2. By choosing which item type user needs
# Accessible actions:
# Login, Register
# Add To Cart: Each item could be added to user's cart at any quantity.
# A store page, where user can access the name, price and picture of items.
@auth.route("/catalog", methods=['GET', 'POST'])
@auth.route("/catalog/<type>", methods=['GET', 'POST'])
def catalog(type=None):
    if type:
        items = Item.query.filter_by(type_id=type)
    else:
        items = Item.query.all()

    logForm = LogForm(prefix="logForm")
    regForm = RegForm(prefix="regForm")
    logout = LogOut(prefix="logout")
    addToCart = AddToCart(prefix="addToCart")
    types = Type.query.all()

    if regForm.validate_on_submit() and regForm.submitReg.data:
        if User.query.filter_by(email=regForm.emailVal.data).first():
            return redirect(url_for('auth.landing'))
        new_user = User(email=regForm.emailVal.data)
        new_user.set_password(regForm.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_conf_token()
        send_confirm(new_user, token)
        login_user(new_user)
        return render_template('auth/follow_email.html')

    if logForm.validate_on_submit() and logForm.submitIn.data:
        user = User.query.filter_by(email=logForm.emailVal.data).first()
        if user is not None and user.password_verify(logForm.password.data):
            login_user(user)
            return redirect(url_for('auth.catalog'))

    if logout.validate_on_submit() and logout.submitOut.data:
        logout_user()
        return render_template('pages/catalog.html', logform=logForm, regform=regForm,
                               logout=logout, items=items, types=types, addToCart=addToCart)

    if addToCart.validate_on_submit() and addToCart.submitAdd.data:
        if current_user.is_authenticated:
            item_id = request.form.get('item_id')
            new_item = cart_items.insert().values(user_id=current_user.id, item_id=item_id)
            db.session.execute(new_item)
            db.session.commit()
            return render_template('pages/catalog.html', logform=logForm, regform=regForm,
                                   logout=logout, items=items, types=types, addToCart=addToCart)

    return render_template('pages/catalog.html', logform=logForm, regform=regForm,
                           logout=logout, items=items, types=types, addToCart=addToCart)


# Add item page, which is only accessible to Moderators and higher. Accessible action:
# Add: form that gets: name, url for picture, type of item and price to decimal
# Once Form is submitted, the item is committed to database. Since then, it is accessible
# for any user to add it to their cart
@auth.route('/add', methods=['GET', 'POST'])
@permission_required(2)
def add():
    addProduct = AddProduct(prefix="addProduct")
    logout = LogOut(prefix="logout")

    if addProduct.validate_on_submit() and addProduct.add.data:
        new_item = Item(
            name=addProduct.name.data,
            picture=addProduct.picture.data,
            type_id=addProduct.type_id.data,
            price=addProduct.price.data
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('auth.catalog'))

    if logout.validate_on_submit() and logout.submitOut.data:
        logout_user()
        return render_template('pages/catalog.html', logform=logForm, regform=regForm,
                               logout=logout, items=items, types=types, addToCart=addToCart)

    return render_template('pages/add.html', addProduct=addProduct)


# Confirmation link. In a mail, that a new user receives they get a link. After clicking on one,
# user confirms their email.
@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return render_template('auth/registration_success.html')
    if current_user.confirm(token):
        db.session.commit()
    return render_template('auth/registration_success.html')


# With registration, user will receive a letter with a confirmation link.
# send_confirm, send_mail and send_async_mail stand for sending user a mail.
def send_confirm(user, token):
    logForm = LogForm(prefix="logForm")
    regForm = RegForm(prefix="regForm")
    logout = LogOut(prefix="logout")
    send_mail(user.email, 'Create your account', 'auth/confirm', user=user, token=token.decode('utf-8'))
    return render_template('pages/landing.html', logform=logForm, regform=regForm, logout=logout)


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender="alextesttestovik@gmail.com", recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    from app import app_main
    thread = Thread(target=send_async_mail, args=[app_main, msg])
    thread.start()
    return thread


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)
