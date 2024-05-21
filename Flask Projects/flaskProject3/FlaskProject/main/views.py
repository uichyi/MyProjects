import random

from . import main
from flask import request, make_response, render_template, abort, session, flash, url_for, redirect
from flask_mail import Message
from FlaskProject.models import User, Item, Type, cart_items
from flask_login import current_user
from FlaskProject import mail, db
from FlaskProject.decorators import permission_required


# An Easter egg function.
@main.route('/teapot', methods=['POST'])
def teapot():
    abort(418)


# Checking whether current user's browser is mozilla or not.
# If it is, random cookie from 1 to 50 will be set
# If it's not, user will receive a message.
# Incorrectly working. More of an Easter egg function than a functional one.
@main.route("/cookie")
def mozilla_cookie():
    sec = request.headers.get('sec-ch-ua')
    if 'mozilla' in sec.lower():
        flag = random.randint(1, 50)
        res = make_response("<h2>Cookie is set<h2>")
        res.set_cookie('flag', str(flag))
        return res
    else:
        return "<h2>Your browser is not supported!<h2>"
