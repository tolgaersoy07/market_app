from flask import Blueprint, request, jsonify,render_template
import mysql.connector
from db import get_db_connection  
from token_services import get_email_from_token

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/orders')
def orders():
    return render_template('orders.html')

@orders_bp.route('/orders_validate', methods=['GET'])
def orders_validate():
    try:
        page_number=request.args.get('page',1,type=int)
        LIMIT=request.args.get('per_page',5,type=int)
        START=(page_number-1)*LIMIT
        token=request.headers.get('Authorization')
        email=get_email_from_token(token)
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cursor.fetchone()['id']
     
        cursor.execute("SELECT COUNT(DISTINCT o.id) AS total FROM orders o WHERE o.user_id = %s", (user_id,))
        total_orders = cursor.fetchone()["total"]
        cursor.execute("SELECT id FROM orders WHERE user_id=%s  ORDER BY id DESC LIMIT %s OFFSET %s;", (user_id, LIMIT, START))
        query_order = cursor.fetchall()

        if not query_order:
            return jsonify([]), 200

        order_ids = [order["id"] for order in query_order]
        format_strings = ','.join(['%s'] * len(order_ids))

        query = f"""
        SELECT 
        o.id AS order_id, 
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
        WHERE o.user_id = %s 
        AND o.id IN ({format_strings})  
        ORDER BY  o.id DESC;
        """
        cursor.execute(query, (user_id, *order_ids))  
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
       
   
        if not orders:
            return jsonify({
                "orders": [],
                "total_orders": total_orders,
                "total_products": 0,
                "page": page_number,
                "per_page": LIMIT
            }), 200

        order_dict = {}
        temp=[]
        for row in orders:
            order_id = row["order_id"]
            if order_id not in order_dict:
                order_dict[order_id] = {
                    "Order number": order_id,
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
            "total_products": len(temp),
            "page": page_number,   
            "per_page": LIMIT
        })
    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": "Database error", "details": str(err)}), 500
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500