from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from flask import current_app as app
import datetime

from .models.user import User
from .models.orders import Orders


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))
    address = StringField(_l('Address'), validators=[DataRequired()])

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))


    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/dash/<user_id>')
def dash(user_id):
    order_history = Orders.get_all_by_uid_since(
            user_id, datetime.datetime(1980, 9, 14, 0, 0, 0))

    account_balance = User.get_account_balance(user_id)
    user = User.get(user_id)
    seller_name = User.get_seller(user_id)
    app.logger.error(seller_name)
    return render_template('dash.html', order_history=order_history
                                      , account_balance=account_balance
                                      , user=user
                                      , seller_name=seller_name)

@bp.route('/add_balance/<user_id>', methods=['POST', 'GET'])
def add_balance(user_id):
    balance = request.form['balance']
    User.add_balance(user_id, balance)

    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/withdraw_balance/<user_id>', methods=['POST', 'GET'])
def withdraw_balance(user_id):
    balance = request.form['balance']
    User.withdraw_balance(user_id, balance)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_fname/<user_id>', methods=['POST', 'GET'])
def change_fname(user_id):
    change = request.form['change']
    User.change_fname(user_id, change)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_lname/<user_id>', methods=['POST', 'GET'])
def change_lname(user_id):
    change = request.form['change']
    User.change_lname(user_id, change)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_email/<user_id>', methods=['POST', 'GET'])
def change_email(user_id):
    change = request.form['change']
    User.change_email(user_id, change)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_address/<user_id>', methods=['POST', 'GET'])
def change_address(user_id):
    change = request.form['change']
    User.change_address(user_id, change)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_password/<user_id>', methods=['POST', 'GET'])
def change_password(user_id):
    change = request.form['change']
    User.change_password(user_id, change)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_store/<user_id>', methods=['POST', 'GET'])
def change_store(user_id):
    change = request.form['change']
    User.change_store(user_id, change)
    return redirect(url_for('users.dash', user_id=user_id))
