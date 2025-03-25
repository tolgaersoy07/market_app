from flask import Blueprint, request, jsonify, make_response, redirect
import jwt
from db import get_db_connection  # Veritabanı bağlantı modülün
from token_services import get_email_from_token  # Token'dan email alma fonksiyonu

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['GET'])
def logout():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"message": "Token bulunamadı"}), 400

    try:
        email = get_email_from_token(token)  # Token'dan email alma fonksiyonun
    except jwt.InvalidTokenError:
        return jsonify({"message": "Geçersiz token"}), 401

    # Veritabanından refresh token'ı sil
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM refresh_tokens WHERE email = %s", (email,))
    conn.commit()
    conn.close()

    # Yanıtı oluştur ve çerezi sil
    response = make_response(jsonify({"message": "Çıkış başarılı"}))
    response.delete_cookie('deviceID_marketapp', path='/', domain=None, httponly=True)

    return response