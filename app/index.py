from flask import current_app as app
from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.selling import Selling
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
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
                           purchase_history=purchases)


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
