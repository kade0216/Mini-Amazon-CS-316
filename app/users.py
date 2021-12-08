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
from .models.seller import Seller
from .models.orders import Orders
from .models.seller_review import Seller_Review


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

@bp.route('/dash/<user_id>', methods=['GET', 'POST'])
@bp.route('/dash/<user_id>/<filter>', methods=['GET', 'POST'])
def dash(user_id, filter=False):
    account_balance = User.get_account_balance(user_id)
    user = User.get(user_id)
    seller = Seller.get(user_id)

    if seller:
        seller_name = seller.seller_name
    else:
        seller_name = None

    full_order_history = Orders.get_order_history(user_id)

    dd = {}
    dp = {}
    ds = {}
    for order in full_order_history:
        year = order.time_purchased.year
        if year not in dd:
            dd[year] = 0
            dp[year] = 0
            ds[year] = set([])
        dd[year] += order.final_price
        dp[year] += order.quantity
        ds[year].add(order.seller_id)

    sorted_dd = sorted(dd.items())
    sorted_dp = sorted(dp.items())
    sorted_ds = sorted(ds.items())

    dollar_labels = [year for year,price in sorted_dd]
    dollar_values = [price for year,price in sorted_dd]

    prod_labels = [year for year,occ in sorted_dp]
    prod_values = [occ for year,occ in sorted_dp]

    seller_labels = [year for year,occ in sorted_ds]
    seller_values = [len(occ) for year,occ in sorted_ds]



    if bool(filter) == True:
        since = datetime.datetime.now() - datetime.timedelta(int(request.form['since']))
        item_search = request.form['item_search']
        seller_search = request.form['seller_search']
        get_order_history_grouped_by_timestamp  = Orders.get_order_history_grouped_by_timestamp(
            user_id,
            since,
            item_search,
            seller_search)


        return render_template('dash.html', order_history=get_order_history_grouped_by_timestamp,
                                            account_balance=account_balance,
                                            user=user,
                                            seller_name=seller_name,
                                            since=since.strftime("%m/%d/%y"),
                                            since_days=int(request.form['since']),
                                            item_search=item_search,
                                            seller_search=seller_search,
                                            page_num=request.form.get('page'),
                                            dollar_values=dollar_values,
                                            dollar_labels=dollar_labels,
                                            prod_values=prod_values,
                                            prod_labels=prod_labels,
                                            seller_values=seller_values,
                                            seller_labels=seller_labels)

    get_order_history_grouped_by_timestamp = Orders.get_order_history_grouped_by_timestamp(current_user.id)

    return render_template('dash.html', order_history=get_order_history_grouped_by_timestamp,
                                        account_balance=account_balance,
                                        user=user,
                                        seller_name=seller_name,
                                        page_num=1,
                                        dollar_values=dollar_values,
                                        dollar_labels=dollar_labels,
                                        prod_values=prod_values,
                                        prod_labels=prod_labels,
                                        seller_values=seller_values,
                                        seller_labels=seller_labels)

@bp.route('/become_seller/<user_id>', methods=['POST', 'GET'])
def become_seller(user_id):
    seller_name = request.form['seller_name']

    if (Seller.does_seller_exist(seller_name)):
        flash(f"{seller_name} already exists! Choose a different seller name.")
        return redirect(url_for('users.dash', user_id=user_id))

    else:
        Seller.become_seller(user_id, seller_name)
        return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/add_balance/<user_id>', methods=['POST', 'GET'])
def add_balance(user_id):
    balance = request.form['balance']
    User.change_balance(user_id, balance, '+')

    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/withdraw_balance/<user_id>', methods=['POST', 'GET'])
def withdraw_balance(user_id):
    balance = request.form['balance']
    User.change_balance(user_id, balance, '-')
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_fname/<user_id>', methods=['POST', 'GET'])
def change_fname(user_id):
    new = request.form['change']
    User.change_info(user_id, 'firstname', new)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_lname/<user_id>', methods=['POST', 'GET'])
def change_lname(user_id):
    new = request.form['change']
    User.change_info(user_id, 'lastname', new)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_email/<user_id>', methods=['POST', 'GET'])
def change_email(user_id):
    new = request.form['change']
    User.change_info(user_id, 'email', new)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_address/<user_id>', methods=['POST', 'GET'])
def change_address(user_id):
    new = request.form['change']
    User.change_info(user_id, 'address', new)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_password/<user_id>', methods=['POST', 'GET'])
def change_password(user_id):
    new = request.form['change']
    User.change_info(user_id, 'password', new)
    return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/change_store/<user_id>', methods=['POST', 'GET'])
def change_store(user_id):
    change = request.form['change']
    if (Seller.does_seller_exist(change)):
        flash(f"{change} already exists! Choose a different seller name.")
        return redirect(url_for('users.dash', user_id=user_id))
    else:
        User.change_store(user_id, change)
        return redirect(url_for('users.dash', user_id=user_id))

@bp.route('/user_profile/<user_id>')
def get_public_user_page(user_id):
    user = User.get(user_id)
    if Seller.get(user_id) is not None:
        seller = Seller.get(user_id)
        seller_avg = round(Seller_Review.get_summary_for_seller(user_id)[0],2)
        seller_count = round(Seller_Review.get_summary_for_seller(user_id)[1],2)
        seller_review_list = Seller_Review.get_all_reviews_for_seller(user_id)
        for seller_review in seller_review_list:
            uid = seller_review.buyer_id
            userTemp = User.get(uid)
            reviewer_name = userTemp.firstname + " " + userTemp.lastname
            seller_review.reviewer_name = reviewer_name

        if current_user.is_authenticated:
            logged_in = True
            if Seller_Review.review_exists(user_id, current_user.id):
                rating_exists = True
                review = Seller_Review.get(user_id,current_user.id)
                rating = review.rating
                reviewText= review.reviewText
                return render_template('user_public_page.html', logged_in=logged_in,rating_exists=rating_exists,rating=rating,reviewText=reviewText,user=user,isSeller=True,seller=seller,seller_review_list=seller_review_list,seller_avg=seller_avg,seller_count=seller_count)

            else:
                rating_exists = False
                rating=-1
                reviewText= ""
        else:
            logged_in = None
            rating_exists=False
            rating=-1
            reviewText= ""

        return render_template('user_public_page.html', logged_in=logged_in,rating_exists=rating_exists,rating=rating,reviewText=reviewText,user=user,isSeller=True,seller=seller,seller_review_list=seller_review_list,seller_avg=seller_avg,seller_count=seller_count)

    else:
        return render_template('user_public_page.html', user=user,seller=False)

@bp.route('/dash/detailed_order_page/<timestamp>')
def get_detailed_order_page(timestamp):
    orders = Orders.get_single_order(current_user.id, timestamp)

    return render_template('detailed_order_page.html', timestamp=timestamp, orders=orders)

@bp.route('/sorted_seller_page/<seller_id>', methods=['GET','POST'])
def get_sorted_seller_page(seller_id):

    sort = request.form['sortSeller']
    user = User.get(seller_id)
    if Seller.get(seller_id) is not None:
        seller = Seller.get(seller_id)
        seller_review_list = Seller_Review.get_all_reviews_for_seller(seller_id)
        for seller_review in seller_review_list:
            uid = seller_review.buyer_id
            userTemp = User.get(uid)
            reviewer_name = userTemp.firstname + " " + userTemp.lastname
            seller_review.reviewer_name = reviewer_name

        if sort=='reverse_chronological':
            seller_review_list.sort(key=lambda x: x.date)
            seller_review_list.reverse()
        elif sort=='chronological':
            seller_review_list.sort(key=lambda x: x.date)
        elif sort=='rating_high_to_low':
            seller_review_list.sort(key=lambda x: x.rating)
            seller_review_list.reverse()
        elif sort=='rating_low_to_high':
            seller_review_list.sort(key=lambda x: x.rating)
        elif sort=='least_to_most_popular':
            seller_review_list.sort(key=lambda x: x.upvote_count-x.downvote_count)
        elif sort == 'most_to_least_popular':
            seller_review_list.sort(key=lambda x: x.upvote_count-x.downvote_count)
            seller_review_list.reverse()
        else:
            seller_review_list.sort(key=lambda x: x.date)
            seller_review_list.reverse()

        seller_avg = round(Seller_Review.get_summary_for_seller(seller_id)[0],2)
        seller_count = round(Seller_Review.get_summary_for_seller(seller_id)[1],2)

        if current_user.is_authenticated:
            logged_in = True
            if Seller_Review.review_exists(seller_id, current_user.id):
                rating_exists = True
                review = Seller_Review.get(seller_id,current_user.id)
                rating = review.rating
                reviewText= review.reviewText
                return render_template('user_public_page.html', logged_in=logged_in,rating_exists=rating_exists,rating=rating,reviewText=reviewText,user=user,isSeller=True,seller=seller,seller_review_list=seller_review_list,seller_avg=seller_avg,seller_count=seller_count)

            else:
                rating_exists = False
                rating=-1
                reviewText= ""
        else:
            logged_in = None
            rating_exists=False
            rating=-1
            reviewText= ""

        return render_template('user_public_page.html', logged_in=logged_in,rating_exists=rating_exists,rating=rating,reviewText=reviewText,user=user,isSeller=True,seller=seller,seller_review_list=seller_review_list,seller_avg=seller_avg,seller_count=seller_count)
