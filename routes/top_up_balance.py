from flask import Blueprint, request, jsonify, render_template
from mysql.connector import Error
from db import get_db_connection
from token_services import get_email_from_token

top_up_balance_bp = Blueprint('top_up_balance', __name__)

@top_up_balance_bp.route('/top_up_balance')
def top_up_balance():
    return render_template('top_up_balance.html')

@top_up_balance_bp.route('/top_up_balance_process', methods=['POST'])
def top_up_balance_process():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request - No JSON data provided'}), 400
    access_token=request.headers.get('Authorization')
    email = get_email_from_token(access_token)
    balance = data.get('balance')

    if not email or balance is None:
        return jsonify({'error': 'Missing required fields: email and balance'}), 400

    if not isinstance(balance, (int, float)) or balance <= 0:
        return jsonify({'error': 'Balance must be a positive number'}), 400

    # Veritabanı bağlantısını aç
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Kullanıcıyı sorgula
        cursor.execute('SELECT balance,id FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found'}), 404
        #Kredi kartından para çekme işini ayarla burada.
        
        # Güncellenmiş bakiyeyi hesapla
        old_balance = user['balance']
        new_balance = old_balance + balance

        cursor.execute("INSERT INTO topups (user_id,amount) VALUES (%s,%s)",(user['id'],balance))

        # Bakiyeyi güncelle
        cursor.execute('UPDATE users SET balance = %s WHERE email = %s', (new_balance, email))
        conn.commit()

        return jsonify({'code':200,'message': 'Balance updated successfully', 'new_balance': new_balance}), 200

    except Error as e:
        return jsonify({'error': 'Internal Server Error'}), 500

    finally:
        cursor.close()
        conn.close()