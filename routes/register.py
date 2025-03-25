from flask import Blueprint, request, render_template, jsonify
from db import get_db_connection
from hashing_password import password_hashing
import mysql.connector

register_bp = Blueprint('register', __name__)

@register_bp.route('/register')
def register():
    return render_template('register.html')

@register_bp.route('/register_validate', methods=['POST'])
def register_validate():
    try:
        data = request.get_json()
        if not data['first_name'] or not data['last_name'] or not data['email'] or not data['password'] or not data['phone']:
            return jsonify({"message": "Ad, soyad, email, şifre ve telefon zorunludur"}), 400
        
        if len(data['password']) < 5:
            return jsonify({"message": "Şifre en az 5 karakter olmalıdır"}), 400


        first_name = data['first_name'][0].upper() + data['first_name'][1:].lower()
        last_name = data['last_name'].upper()
        email = data['email'].lower()
        password = data['password']
        phone = data['phone']
        hashed_password = password_hashing(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Aynı email ile kayıtlı kullanıcı var mı?
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"message": "Bu email adresi zaten kullanılıyor"}), 409

        # Aynı telefon ile kayıtlı kullanıcı var mı?
        cursor.execute("SELECT id FROM users WHERE phone = %s", (phone,))
        if cursor.fetchone():
            return jsonify({"message": "Bu telefon numarası zaten kullanılıyor"}), 409

        # Kullanıcıyı ekleyelim
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, password_hash, phone) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, email, hashed_password, phone)
        )
        conn.commit()

        return jsonify({"message": "Kullanıcı başarıyla kaydedildi", 'code':200}), 201

    except mysql.connector.Error as e:
        return jsonify({"message": f"Veritabanı hatası: {str(e)}"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
