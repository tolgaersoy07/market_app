from flask import Blueprint, render_template

product_operation_bp = Blueprint("product_operation", __name__, url_prefix="/admin")

@product_operation_bp.route("/product_operation")
def product_operation():
    return render_template("admin/product_operation.html")
