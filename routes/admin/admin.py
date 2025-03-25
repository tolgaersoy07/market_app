from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
def admin_dashboard():
    return render_template("admin/admin_dashboard.html")

