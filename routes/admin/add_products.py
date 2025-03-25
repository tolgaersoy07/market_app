from flask import Blueprint, render_template

add_products_bp = Blueprint("add_products", __name__, url_prefix="/admin")

@add_products_bp.route("/add_products")
def add_products():
    return render_template("admin/add_products.html")


