from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

from .models.selling import Selling
from .models.orders import Orders

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

@bp.route("/seller/remove_item/<product_name>", methods=["POST"])
def remove_product_from_seller_inventory(product_name):

    Selling.remove_product_from_seller_inventory(current_user.id, product_name)

    return redirect(url_for("seller.get_seller_inventory_page"))

@bp.route("/seller/get_order_history", methods=["GET"])
def display_order_history():
    return render_template('orders.html',
                           order_history=Orders.get_all_for_seller(current_user.id))

@bp.route("/seller/fufill_order/<buyer_id>/<time_purchased>/<product_name>", methods=["GET", "POST"])
def fufill_order(buyer_id, time_purchased, product_name):

    Orders.fufill_order(buyer_id, time_purchased, current_user.id, product_name)

    return redirect(url_for("seller.display_order_history"))
