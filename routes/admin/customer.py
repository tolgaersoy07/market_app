from flask import Blueprint, render_template

customer_bp = Blueprint("customer", __name__, url_prefix="/admin")

@customer_bp.route("/customer")
def customer():
    return render_template("admin/customer.html")
print("swdssd")
