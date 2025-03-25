from flask import Blueprint, render_template,request, jsonify
from db import get_db_connection


sales_bp = Blueprint("sales", __name__, url_prefix="/admin")

@sales_bp.route("/sales")
def sales():
    return render_template("admin/sales.html")

@sales_bp.route('/sales_validate', methods=['GET'])
def sales_validate():
    try:
        print("ORDER WORKS")
        # Sayfalama için parametreleri al
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)  # Varsayılan 5 sipariş
        
        # Parametreleri al
        start_date = request.args.get('startDate', '')
        end_date = request.args.get('endDate', '')
        barcode = request.args.get('barcode', '')
        print("start_date",start_date)
        print("end_date",end_date)
        print("barcode",barcode)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Toplam sipariş sayısını al (user_id yok, tüm kullanıcılar için)
        cursor.execute("SELECT COUNT(*) AS total FROM orders")
        total_orders = cursor.fetchone()["total"]

        # Filtreleme için sorgu başlat
        query = """
        SELECT 
            o.id AS order_id, 
            o.user_id,
            o.total_price, 
            o.created_at, 
            oi.quantity AS product_quantity, 
            p.name AS product_name, 
            p.info AS product_info, 
            p.price AS product_price, 
            p.barcode AS product_barcode
        FROM orders o
        INNER JOIN order_items oi ON o.id = oi.order_id
        INNER JOIN products p ON oi.product_id = p.id
        """

        # Eğer başlangıç tarihi varsa sorguya ekle
        if start_date:
            query += " AND o.created_at >= %s"
        
        # Eğer bitiş tarihi varsa sorguya ekle
        if end_date:
            query += " AND o.created_at <= %s"
        
        # Eğer barkod varsa sorguya ekle
        if barcode:
            query += " AND p.barcode = %s"

        # Sayfalama için sorguyu tamamla
        query += " ORDER BY o.created_at DESC LIMIT %s OFFSET %s"
        
        # Parametreler
        params = []
        if start_date:
            params.append(start_date)
        if end_date:
            params.append(end_date)
        if barcode:
            params.append(barcode)
        offset = (page - 1) * per_page
        params.extend([per_page, offset])

        cursor.execute(query, tuple(params))
        orders = cursor.fetchall()

        cursor.close()
        conn.close()

        if not orders:
            return jsonify({"orders": [], "total_orders": total_orders, "page": page, "per_page": per_page}), 200

        # Siparişleri gruplama
        order_dict = {}
        for row in orders:
            order_id = row["order_id"]
            if order_id not in order_dict:
                order_dict[order_id] = {
                    "Order number": order_id,
                    "User ID": row["user_id"],
                    "Total amount": row["total_price"],
                    "Order date": row["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
                    "Total products": 0,
                    "Products": []
                }
            order_dict[order_id]["Products"].append({
                "Product name": row["product_name"],
                "Product info": row["product_info"],
                "Product price": row["product_price"],
                "Product barcode": row["product_barcode"],
                "Product quantity": row["product_quantity"]
            })

            order_dict[order_id]["Total products"] += row["product_quantity"]

        return jsonify({
            "orders": list(order_dict.values()), 
            "total_orders": total_orders, 
            "page": page, 
            "per_page": per_page
        })

    except mysql.connector.Error as err:
        return jsonify({"error": "Database error", "details": str(err)}), 500

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

