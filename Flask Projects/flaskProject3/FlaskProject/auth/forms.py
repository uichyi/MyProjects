from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo, Email, Length

from FlaskProject.models import User, Type


class AddProduct(FlaskForm):
    name = StringField("Name", validators=[Length(1, 64)])
    picture = StringField("URL", validators=[Length(1, 255)])
    type_id = SelectField("Product Type", coerce=int)
    price = DecimalField("Price", places=2)
    add = SubmitField("Add")

    def __init__(self, *args, **kwargs):
        super(AddProduct, self).__init__(*args, **kwargs)
        self.type_id.choices = [(type.id, type.type) for type in Type.query.all()]


class LogForm(FlaskForm):
    emailVal = StringField("Email", validators=[Email(), DataRequired(), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired()])
    submitIn = SubmitField("Log In")


class RegForm(FlaskForm):
    emailVal = StringField("Email", validators=[Email(), DataRequired(), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired()])
    password_check = PasswordField("Repeat password", validators=[EqualTo('password', message='Passwords must match')])
    submitReg = SubmitField("Sign In")

    @staticmethod
    def validate_email(field):
        if User.query.filter_by(emailVal=field.data).first():
            raise ValidationError("This email is already in use")


class AddToCart(FlaskForm):
    submitAdd = SubmitField("Add to cart")


class RemoveFromCart(FlaskForm):
    submitRem = SubmitField("Remove")


class LogOut(FlaskForm):
    submitOut = SubmitField("Log Out")
