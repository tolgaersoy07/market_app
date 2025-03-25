from flask import Blueprint, render_template,jsonify

product_list_bp = Blueprint("product_list", __name__, url_prefix="/admin")

@product_list_bp.route("/product_list")
def product_list():
    return render_template("admin/product_list.html")

# Örnek ürün verileri
products = {
    1: {"name": "Ürün A", "stock": 50, "price": 100},
    2: {"name": "Ürün B", "stock": 30, "price": 200},
    3: {"name": "Ürün C", "stock": 20, "price": 150},
}

@product_list_bp.route("/product_info/<int:product_id>")
def product_detail(product_id):
    # Ürün bilgilerini alın
    product = products.get(1)
    print(product,flush=True)
    if product:
        return jsonify({
            "success": True,
            "product": product
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Ürün bulunamadı!"
        }), 404