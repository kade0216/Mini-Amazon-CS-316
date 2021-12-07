from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

from .models.selling import Selling
from .models.orders import Orders
from .models.product import Product

from flask import Blueprint

bp = Blueprint("seller", __name__)

"""All routes concerning the functions of sellers"""

@bp.route('/seller-inventory', methods=['GET'])
def get_seller_inventory_page():
    seller_inventory = Selling.get_all_for_seller(current_user.id)

    return render_template('sellerinventory.html',
                           seller_inventory=seller_inventory)

@bp.route("/seller/add_quant/<product_name>", methods=["POST"])
def add_quantity_to_inventory_item(product_name):
    quantity_diff = request.form["quantity_diff"]
    Selling.change_product_quantity(
        current_user.id, product_name, int(quantity_diff)
    )

    return redirect(url_for("seller.get_seller_inventory_page"))

@bp.route("/seller/subtract_quant/<product_name>", methods=["POST"])
def subtract_quantity_from_inventory_item(product_name):
    quantity_diff = request.form["quantity_diff"]
    Selling.change_product_quantity(
        current_user.id, product_name,int(quantity_diff) * -1
    )

    return redirect(url_for("seller.get_seller_inventory_page"))

@bp.route("/seller/change_price/<product_name>", methods=["POST"])
def change_product_price(product_name):
    price_change = request.form["price_change"]
    Product.change_product_price(
        current_user.id, product_name,int(price_change)
    )

    return redirect(url_for("seller.get_seller_inventory_page"))


@bp.route("/seller/remove_item/<product_name>", methods=["POST"])
def remove_product_from_seller_inventory(product_name):

    Selling.remove_product_from_seller_inventory(current_user.id, product_name)

    return redirect(url_for("seller.get_seller_inventory_page"))

@bp.route("/seller/get_order_history", methods=["GET"])
def display_order_history():
    return render_template('orders.html',
                           order_history=Orders.get_all_for_seller(current_user.id))

@bp.route("/seller/create_product_page", methods=['POST', "GET"])
def create_new_product_page():

    categories = Product.get_categories()

    all_products = Product.get_all_product_names()

    return render_template('create_products.html',
                            categories=categories,
                            all_products=all_products)

@bp.route("/seller/create_product", methods=['POST', "GET"])
def create_new_product():
    """Route is responsible for serving the creation of NEW products """

    #TODO(REPORT ERRORS TO USERS)

    if request.method == "POST":
        name = request.form['new_product_name']
        description = request.form['new_product_des']
        product_quantity = request.form['new_product_quantity']
        price = request.form['new_product_price']
        url = request.form['new_product_image']
        category = request.form['category']

    seller_id = current_user.id

    Product.create_new_product(seller_id, name, category, url, description, price, product_quantity)

    categories = Product.get_categories()

    return redirect(url_for("seller.get_seller_inventory_page"))

@bp.route("/seller/add_product", methods=['POST', "GET"])
def add_new_product():
    """
    Route is responsible for serving the addition of exisiting products on amazon
    (that are not already in the seller's inventory)
    """

    #TODO(REPORT ERRORS TO USERS)
    #TODO(Handle case where we need to make a product available if quantity > 1)


    if request.method == "POST":
        name = request.form['selected-product']
        product_quantity = request.form['new_product_quantity']
        price = request.form['new_product_price']

    seller_id = current_user.id

    Product.add_new_product_to_seller(seller_id, name, price, product_quantity)

    categories = Product.get_categories()

    return redirect(url_for("seller.get_seller_inventory_page"))



@bp.route("/seller/fufill_order/<buyer_id>/<time_purchased>/<product_name>", methods=["GET", "POST"])
def fufill_order(buyer_id, time_purchased, product_name):

    Orders.fufill_order(buyer_id, time_purchased, current_user.id, product_name)

    return redirect(url_for("seller.display_order_history"))
