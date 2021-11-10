from flask import current_app as app
from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.selling import Selling
from .models.cart import Cart
from .models.product_review import Product_Review
from .models.seller_review import Seller_Review


from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)

    categories = Product.get_categories()

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = []
    #     purchases = Purchase.get_all_by_uid_since(
    #         current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None


    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           categories=categories)


@bp.route('/seller-inventory/<user_id>', methods=['GET'])
def get_seller_inventory_page(user_id):
    seller_inventory = Selling.get_all_for_seller(user_id)
    
    '''TODO(Sellers Guru (vikramrk)): Handle login '''

    return render_template('sellerinventory.html',
                           seller_inventory=seller_inventory)


@bp.route('/cart/<user_id>', methods=['GET'])
def get_users_cart(user_id):
    cart = Cart.get_current_cart(user_id)
    return render_template('cart.html', cart=cart)

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
    print(name)
    products = Product.get(name)

    print(products)
    '''TODO(Karan): Handle login '''

    return render_template('productpage.html', product=products)

@bp.route('/product_category/<category>', methods=['GET'])
def get_cat_page(category):
    #print(category)
    prod_in_cat = Product.get_products_in_category(category)

    #print(prod_in_cat)
    return render_template('productcat.html', products=prod_in_cat)


@bp.route('/product_sort_low_to_high', methods=['GET'])
def get_product__sort_low_to_high():

    products_low_to_high = Product.sort_by_price_low_to_high(True)

    print(products_low_to_high)
    '''TODO(Karan): Handle login '''

    return render_template('productpage.html', product=products_low_to_high)

@bp.route('/product_sort_high_to_low', methods=['GET'])
def get_product__sort_high_to_low():

    products_high_to_low = Product.sort_by_price_high_to_low(True)

    '''TODO(Karan): Handle login '''

    return render_template('productpage.html', product=products_high_to_low)
