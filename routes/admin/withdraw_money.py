from flask import Blueprint, render_template

withdraw_money_bp = Blueprint("withdraw_money", __name__, url_prefix="/admin")

@withdraw_money_bp.route("/withdraw_money")
def withdraw_money():
    return render_template("admin/withdraw_money.html")
