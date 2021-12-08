from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

from .models.cart import Cart
from .models.saved_for_later import SavedForLater
from .models.seller import Seller

from flask import Blueprint

bp = Blueprint("cart", __name__)

"""All routes concerning the user's cart"""


@bp.route("/cart", methods=["GET"])
def get_users_cart():
    cart = Cart.get_current_cart(current_user.id)
    saved_for_later = SavedForLater.get_saved_for_later(current_user.id)
    return render_template("cart.html", cart=cart, saved_for_later=saved_for_later)

@bp.route("/cart/add_item/<product_name>/<seller_id>", methods=["POST"])
def add_item_to_cart(product_name, seller_id):

    quantity_diff = request.form["quantity"]
    Cart.add_item_to_cart(current_user.id, product_name, seller_id, int(quantity_diff))

    flash(f"{product_name} sold by Seller #{seller_id} successfully added to cart!")

    return redirect(url_for("index.get_product_page",name=product_name))

@bp.route("/cart/add_item_cart_from_sfl/<product_name>/<seller_name>/<quantity>")
def add_item_to_cart_from_save_for_later(product_name, seller_name, quantity):

    seller_id = Seller.get_seller_id(seller_name)

    Cart.add_item_to_cart(current_user.id, product_name, seller_id, int(quantity))

    SavedForLater.remove_item_from_saved_for_later(current_user.id, product_name, seller_name)

    return redirect(url_for("cart.get_users_cart"))


@bp.route("/cart/remove_item/<product_name>/<seller_name>", methods=["GET", "POST"])
def remove_item_from_cart(product_name, seller_name):

    Cart.remove_item_from_cart(current_user.id, product_name, seller_name)

    return redirect(url_for("cart.get_users_cart"))


@bp.route("/cart/add_quant/<product_name>/<seller_name>", methods=["POST"])
def add_quantity_to_cart_item(product_name, seller_name):
    quantity_diff = request.form["quantity_diff"]
    Cart.change_product_quantity_in_cart(
        current_user.id, product_name, seller_name, int(quantity_diff)
    )

    return redirect(url_for("cart.get_users_cart"))


@bp.route("/cart/subtract_quant/<product_name>/<seller_name>", methods=["POST"])
def subtract_quantity_to_cart_item(product_name, seller_name):
    quantity_diff = request.form["quantity_diff"]
    Cart.change_product_quantity_in_cart(
        current_user.id, product_name, seller_name, int(quantity_diff) * -1
    )

    return redirect(url_for("cart.get_users_cart"))


@bp.route("/cart/submit_order", methods=["GET"])
def submit_order():
    is_cart_valid = Cart.validate_cart(current_user.id)

    # Valid Cart
    if is_cart_valid[0]:
        Cart.submit_cart_as_order(current_user.id)
    else:
        bad_items = is_cart_valid[1]

        bad_items_output = ""
        for item in bad_items:
            bad_items_output += f"\n{item.product_name} sold by {item.seller_name}, "

        app.logger.error(bad_items_output)

        flash(
            f"Error: The cart could not be submitted because the following item's "
            f"quantity in cart exceed their corresponding quantity in inventory: {bad_items_output}"
        )

    return redirect(url_for("cart.get_users_cart"))

@bp.route("/cart/add_item_sfl/<product_name>/<seller_id>", methods=["POST"])
def add_item_to_save_for_later(product_name, seller_id):

    quantity_diff = request.form["quantity"]
    SavedForLater.add_item_to_saved_for_later(current_user.id, product_name, seller_id, int(quantity_diff))

    flash(f"{product_name} sold by Seller #{seller_id} successfully saved for later!")

    return redirect(url_for("cart.get_users_cart"))

@bp.route("/cart/add_item_to_save_for_later_from_cart/<product_name>/<seller_name>/<quantity>")
def add_item_to_save_for_later_from_cart(product_name, seller_name, quantity):
    seller_id = Seller.get_seller_id(seller_name)
    SavedForLater.add_item_to_saved_for_later(current_user.id, product_name, seller_id, int(quantity))
    Cart.remove_item_from_cart(current_user.id, product_name, seller_name)

    return redirect(url_for("cart.get_users_cart"))

@bp.route("/cart/remove_item_sfl/<product_name>/<seller_name>", methods=["GET", "POST"])
def remove_item_from_saved_for_later(product_name, seller_name):

    SavedForLater.remove_item_from_saved_for_later(current_user.id, product_name, seller_name)

    return redirect(url_for("cart.get_users_cart"))

@bp.route("/cart/add_quant_sfl/<product_name>/<seller_name>", methods=["POST"])
def add_quantity_to_saved_for_later_item(product_name, seller_name):
    quantity_diff = request.form["quantity_diff"]
    SavedForLater.change_product_quantity_in_saved_for_later(
        current_user.id, product_name, seller_name, int(quantity_diff)
    )

    return redirect(url_for("cart.get_users_cart"))

@bp.route("/cart/subtract_quant_sfl/<product_name>/<seller_name>", methods=["POST"])
def subtract_quantity_to_saved_for_later_item(product_name, seller_name):
    quantity_diff = request.form["quantity_diff"]
    SavedForLater.change_product_quantity_in_saved_for_later(
        current_user.id, product_name, seller_name, int(quantity_diff) * -1
    )

    return redirect(url_for("cart.get_users_cart"))
