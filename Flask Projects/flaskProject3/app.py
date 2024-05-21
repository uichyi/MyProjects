import unittest
from FlaskProject.models import User, Item, cart_items, Type
from FlaskProject import create_app, db
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import url_for, redirect

app_main = create_app('default')
migrate = Migrate(app_main, db)


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.permission.value >= 3


admin = Admin(app_main)
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Item, db.session))
admin.add_view(AdminModelView(Type, db.session))


@app_main.cli.command('test')
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
