from flask import Blueprint, request, render_template, jsonify
from db import get_db_connection

scan_barcode_bp = Blueprint('scan_barcode', __name__)

@scan_barcode_bp.route('/scan_barcode_validate')

@scan_barcode_bp.route('/scan_barcode')
def scan_barcode():
    return render_template('scan_barcode.html')

@scan_barcode_bp.route('/get_product_info/<barcode>', methods=['GET'])
def get_product(barcode):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Barkoda göre ürün sorgulama
    query = "SELECT id, name, info, barcode, price, stock_quantity FROM products WHERE barcode = %s"
    cursor.execute(query, (barcode,))
    product = cursor.fetchone()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    product_id, name, info, barcode, price, stock_quantity = product
    return jsonify({
        "id": product_id,
        "name": name,
        "info": info,
        "barcode": barcode,
        "price": price,
        "stock_quantity": 1
    }), 200
