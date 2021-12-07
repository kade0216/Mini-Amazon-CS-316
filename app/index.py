from flask import current_app as app
from flask import render_template
from flask.ctx import RequestContext
from flask_login import current_user
from flask import request
import datetime
from flask import redirect, url_for

from .models.product import Product
from .models.selling import Selling
from .models.product_review import Product_Review
from .models.seller_review import Seller_Review
from .models.user import User

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    categories = Product.get_categories()

    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           categories=categories,
                           page_num=1)

@bp.route('/user-product-reviews/<user_id>', methods=['GET'])
def get_product_reviews_by_user(user_id):
    review_list = Product_Review.get_all_reviews_by_buyer(user_id)

    return render_template('user_product_reviews.html',
                 review_list=review_list)

@bp.route('/user-seller-reviews/<user_id>', methods=['GET'])
def get_seller_reviews_by_user(user_id):
    review_list = Seller_Review.get_all_reviews_by_buyer(user_id)

    return render_template('user_seller_reviews.html',
                 review_list=review_list)


@bp.route('/reviews-for-product/<product_name>', methods=['GET'])
def get_reviews_for_product(product_name):
    product_name = "'" + product_name.replace("_", " ") + "'"
    review_list = Product_Review.get_all_reviews_for_product(product_name)

    return render_template('reviews_for_product.html',
                 review_list=review_list)

@bp.route('/reviews-for-seller/<seller_id>', methods=['GET'])
def get_reviews_for_seller(seller_id):
    review_list = Seller_Review.get_all_reviews_for_seller(seller_id)

    return render_template('reviews_for_seller.html',
                 review_list=review_list)


@bp.route('/product_page/<name>', methods=['GET'])
def get_product_page(name):
    products = Product.get(name)
    product_review_list = Product_Review.get_all_reviews_for_product(name)
    avail = Product.is_product_available(name)
    for product_review in product_review_list:
        uid = product_review.buyer_id
        user = User.get(uid)
        reviewer_name = user.firstname + " " + user.lastname
        product_review.reviewer_name = reviewer_name

    if current_user.is_authenticated:
        logged_in = True
        if Product_Review.review_exists(name, current_user.id):
            rating_exists = True
            review = Product_Review.getRating(name,current_user.id)
            rating = review.rating
            reviewText= review.reviewText
        else:
            rating_exists = False
            rating=-1
            reviewText= ""
    else:
        logged_in = None
        rating_exists=False
        rating=-1
        reviewText= ""

    return render_template('productpage.html', name=name, product=products, logged_in=logged_in, review_exists=rating_exists,rating=rating,product_review_list=product_review_list, available=avail, reviewText=reviewText)

@bp.route('/search', methods=['POST', 'GET'])
def get_search_results():
    products = []
    if request.method == "POST":
        search = request.form['search']
        category = request.form['category']
        sort = request.form['sort']

        min_price = request.form['min_product_price']
        max_price = request.form['max_product_price']

        if min_price == '':
            min_price = 0
        if max_price == '':
            max_price = 1000000000

        products = Product.get_search(search, category, min_price, max_price, sort)

    categories = Product.get_categories()

    # render the page by adding information to the index.html file
    return render_template('index.html',
                            avail_products=products,
                            categories=categories,
                            search_params=[search, category, sort.replace('_', ' '), min_price, max_price],
                            item_search=search,
                            category=category,
                            sort=sort,
                            min_price=min_price,
                            max_price=max_price,
                            page_num=request.form.get('page'))

@bp.route('/reviews', methods=['GET'])
def get_reviews_by_user():
    seller_review_list = Seller_Review.get_all_reviews_by_buyer(current_user.id)
    product_review_list = Product_Review.get_all_reviews_by_buyer(current_user.id)
    seller_review_list.sort(key=lambda x: x.date)
    seller_review_list.reverse()
    product_review_list.sort(key=lambda x: x.date)
    product_review_list.reverse()

    return render_template('user_reviews.html',
                     seller_review_list=seller_review_list,
                     product_review_list=product_review_list)

@bp.route('/reviews-edit-product/<product_name>',methods=['GET','POST'])
def get_reviews_by_user_with_product_edit(product_name):
    seller_review_list = Seller_Review.get_all_reviews_by_buyer(current_user.id)
    product_review_list = Product_Review.get_all_reviews_by_buyer(current_user.id)
    seller_review_list.sort(key=lambda x: x.date)
    seller_review_list.reverse()
    product_review_list.sort(key=lambda x: x.date)
    product_review_list.reverse()

    product_review_to_edit = Product_Review.getRating(product_name, current_user.id)

    return render_template('user_reviews_with_product_edit.html',
                     seller_review_list=seller_review_list,
                     product_review_list=product_review_list,
                     product_review_to_edit=product_review_to_edit)



@bp.route('/add_review_product/<product_name>', methods=['POST'])
def add_review_product(product_name):
    rating = request.form['rating']
    review = request.form['review']

    Product_Review.add_review(product_name, current_user.id, rating, review)
    return redirect(url_for('index.get_product_page', name=product_name))

@bp.route('/change_product_rating/<product_name>/<summary>', methods=['POST'])
def change_product_rating(product_name,summary):
    newRating = request.form['rating']
    newReview = request.form['review']
    Product_Review.change_rating(product_name, current_user.id, newRating, newReview)
    if summary=='0':
    	return redirect(url_for('index.get_product_page', name=product_name))
    else:
    	return redirect(url_for('index.get_reviews_by_user'))

@bp.route('/delete_product_rating/<product_name>/<summary>', methods=['POST'])
def delete_product_rating(product_name,summary):

    Product_Review.delete_rating(product_name, current_user.id)

    if summary=='0':
    	return redirect(url_for('index.get_product_page', name=product_name))
    else:
    	return redirect(url_for('index.get_reviews_by_user'))


@bp.route('/delete_product_text_review/<product_name>/<summary>', methods=['POST'])
def delete_product_text_review(product_name,summary):

    Product_Review.delete_text_review(product_name, current_user.id)

    if summary=='0':
    	return redirect(url_for('index.get_product_page', name=product_name))
    else:
    	return redirect(url_for('index.get_reviews_by_user'))
