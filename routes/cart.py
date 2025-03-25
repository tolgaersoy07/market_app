from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, timezone
from db import get_db_connection  
from token_services import get_email_from_token

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def cart():
    return render_template('cart.html')

#Sepetteki ürünleri listeleme.
@cart_bp.route('/cart/view', methods=['GET'])
def get_cart_items():
    token = request.headers.get('Authorization')
    email = get_email_from_token(token)
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query="""
        SELECT 
            CI.product_id,
            CI.quantity,
            P.name,
            P.info,
            P.barcode,
            P.price AS unit_price,
            (CI.quantity * P.price) AS total_price,
            P.stock_quantity,
            LEAST(P.stock_quantity, CI.quantity) AS max_available_quantity,
            CASE 
                WHEN P.stock_quantity = 0 THEN 'STOK YOK'
                WHEN P.stock_quantity < CI.quantity THEN 'YETERSİZ STOK'
                ELSE 'STOK VAR'
            END AS stock_status
        FROM carts AS C 
        INNER JOIN cart_items AS CI ON C.id = CI.cart_id 
        INNER JOIN products AS P ON CI.product_id = P.id
        WHERE C.user_id = %s
        ORDER BY CI.id DESC;
        """
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    
        user_id = cursor.fetchone()['id']
        if not user_id:
            return jsonify({"message": "Kullanıcı bulunamadı"}), 404
        
        cursor.execute(query,(user_id,))

        result = cursor.fetchall()
        if not result:
            return jsonify({"message": "Sepetiniz boş"}), 200

        total=0
        for item in result:
            total+=item['total_price']
        total=str(round(total,2))
        result.append({"total_price":total})
        return jsonify(result),200

    except Exception as e:
        return jsonify({"message": "API hatası"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Sepete ürün ekleme. Barkod okununca buradan ürün eklenir.
#Barkod gelir kontrol edilir, stok vs kontrolleri yapılır.
#Daha sonra ürün sepete eklenir veya sepettekki stoğu arttırılır.
@cart_bp.route('/cart/add/<int:barcode>', methods=['POST'])
def add_to_cart(barcode):
    token = request.headers.get('Authorization')
    email = get_email_from_token(token)
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        user_id = user[0]
        cursor.execute("SELECT id FROM carts WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()
        cart_id = cart[0] if cart else None

        if not cart_id:
            cursor.execute("INSERT INTO carts (user_id, expires_at) VALUES (%s, %s)", 
                           (user_id, datetime.now(timezone.utc)))
            conn.commit()
            cart_id = cursor.lastrowid

        cursor.execute("SELECT id, stock_quantity FROM products WHERE barcode = %s", (barcode,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"message": "Ürün sistemde kayıtlı değil!"}), 400

        product_id, stock_quantity = product

        cursor.execute("SELECT quantity FROM cart_items WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
        existing_quantity=cursor.fetchone()
        if not existing_quantity:
            existing_quantity=0
        else:
            existing_quantity=existing_quantity[0]
        if existing_quantity + 1 > stock_quantity:
            return jsonify({"message": "Stokta yeterli ürün yok"}), 400
        if existing_quantity:
            cursor.execute("UPDATE cart_items SET quantity = quantity + 1 WHERE cart_id = %s AND product_id = %s",
                           (cart_id, product_id))
        else:
            cursor.execute("INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s)",
                           (cart_id, product_id, 1))
        conn.commit()
        return jsonify({"message": "Ürün sepete eklendi", "product_id": product_id, "quantity": existing_quantity + 1}), 200

    except Exception as e:
        return jsonify({"message": "Ürün eklenirken bir hata oluştu!"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        
#Sepetteki ürün miktarını arttırıp azaltma API'si.
# process = "plus" , "minus" , "delete" olabilir.
@cart_bp.route('/cart/update/<int:barcode>/<string:process>', methods=['PUT'])
def update_cart_stock(barcode, process):
    if process not in ["plus", "minus", "delete"]:
        return jsonify({"message": "Geçersiz işlem türü!"}), 400
    token = request.headers.get("Authorization")
    email = get_email_from_token(token)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"message": "Kullanıcı bulunamadı"}), 404
        user_id = user[0]

        cursor.execute("SELECT id FROM carts WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()
        if not cart:
            return jsonify({"message": "Sepet bulunamadı"}), 404
        cart_id = cart[0]

        # **Ürünün sepette olup olmadığını kontrol et**
        cursor.execute("""
            SELECT ci.quantity, p.id AS product_id, p.stock_quantity , p.barcode
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.cart_id = %s AND p.barcode = %s
        """, (cart_id, barcode))
        product = cursor.fetchone()

        if not product:
            return jsonify({"message": "Ürün sepette bulunamadı"}), 404

        quantity, product_id, stock_quantity,barcode = product

        if process == "plus":
            if quantity + 1 > stock_quantity:
                return jsonify({"message": "Stokta yeterli ürün yok",'barcode':barcode}), 400
            cursor.execute("UPDATE cart_items SET quantity = quantity + 1 WHERE cart_id = %s AND product_id = %s",
                           (cart_id, product_id))

        elif process == "minus":
            if quantity > 1:
                cursor.execute("UPDATE cart_items SET quantity = quantity - 1 WHERE cart_id = %s AND product_id = %s",
                               (cart_id, product_id))
            else:
                cursor.execute("DELETE FROM cart_items WHERE cart_id = %s AND product_id = %s",
                               (cart_id, product_id))

        elif process == "delete":
            cursor.execute("DELETE FROM cart_items WHERE cart_id = %s AND product_id = %s",
                           (cart_id, product_id))
        conn.commit()
        return jsonify({"message": "Sepet güncellendi!",'code':200}), 200

    except Exception as e:
        return jsonify({"message": "Ürün miktarı güncellenirken hata oluştu!"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#sepetteki ürünleri satın alma apisi.
#ürünler kontrol edilir sepet vs kontrolleri yapılır. sonra alınır. sonra sepette boşaltılır.
@cart_bp.route('/cart/payment', methods=['POST'])
def process_payment():
    token = request.headers.get('Authorization')
    email = get_email_from_token(token) 
    if not email:
        return jsonify({"message": "Yetkisiz erişim!"}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # **Autocommit kontrolü ve transaction başlatma**
        cursor.execute("SELECT @@autocommit;")
        auto_commit = cursor.fetchone()['@@autocommit']
        if auto_commit == 1:
            conn.start_transaction()

        cursor.execute("SELECT id, balance FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"message": "Kullanıcı bulunamadı!"}), 404

        user_id, user_balance = user['id'], user['balance']

        # **Sepet verilerini al**
        cursor.execute("""
            SELECT P.id AS product_id, P.barcode, P.stock_quantity, P.price, CI.quantity 
            FROM carts AS C 
            INNER JOIN cart_items AS CI ON C.id = CI.cart_id 
            INNER JOIN products AS P ON CI.product_id = P.id
            WHERE C.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()

        if not cart_items:
            return jsonify({"message": "Sepetiniz boş!"}), 400

        # **Toplam fiyat hesaplama**
        total_price = sum(item['price'] * item['quantity'] for item in cart_items)

        # **Bakiye kontrolü**
        if user_balance < total_price:
            return jsonify({"message": f"Bakiye yetersiz! Mevcut: {user_balance}₺, Gerekli: {total_price}₺"}), 400

        # **Stok kontrolü**
        for item in cart_items:
            if item['stock_quantity'] < item['quantity']:
                return jsonify({"message": f"{item['barcode']} barkodlu üründen stokta sadece {item['stock_quantity']} adet var!"}), 400

        # **Sipariş oluştur**
        cursor.execute("INSERT INTO orders (user_id, total_price) VALUES (%s, %s)", (user_id, total_price))
        order_id = cursor.lastrowid

        # **Sipariş detaylarını ekle & Stokları düşür**
        for item in cart_items:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                           (order_id, item['product_id'], item['quantity'], item['price']))
            cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE id = %s",
                           (item['quantity'], item['product_id']))

        # **Bakiyeyi düş ve sepeti temizle**
        cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (total_price, user_id))
        cursor.execute("DELETE FROM cart_items WHERE cart_id IN (SELECT id FROM carts WHERE user_id = %s)", (user_id,))
        cursor.execute("DELETE FROM carts WHERE user_id = %s", (user_id,))

        # **Transaction'u tamamla**
        conn.commit()
        return jsonify({'code':200,"message": "Ödeme başarılı, sipariş oluşturuldu!", "order_id": order_id, "total_price": total_price}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"message": f"Hata oluştu: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()