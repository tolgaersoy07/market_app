from flask import Blueprint, request, render_template, jsonify,make_response
from db import get_db_connection
from hashing_password import check_password
from token_services import save_refresh_token_to_db,create_access_token,get_user_type
import secrets

login_bp = Blueprint('login', __name__)

@login_bp.route('/login')
def login():
    return render_template('login.html')

@login_bp.route('/set_cookie', methods=['GET'])
def set_cookie():
    device_id = request.cookies.get('deviceID_marketapp')
    if device_id:
        response = make_response(jsonify({"message": "Cookie zaten var", "random_number": device_id}))
        return response
    random_number = secrets.token_hex(16)
    response = make_response(jsonify({"message": "Cookie set edildi", "random_number": random_number}))
    response.set_cookie(
        'deviceID_marketapp',
        random_number,  
        httponly=True,  
        secure=False, # false yap http çalışşsın
        samesite='Strict',  
        max_age=3600)
    return response

@login_bp.route('/login_validate', methods=['POST'])
def login_validate():
    data =request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'valid':False, 'message': 'Lütfen E-Postanızı ve Şifrenizi eksiksiz doldurunuz!'}), 400
    user_type=get_user_type(email)
    if user_type=="no_one":
        return jsonify({'valid':False, 'message': 'Böyle bir kullanıcı bulunmamaktadır.'}), 401
    user=None
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
   
    if user_type=="user":
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    else:
        cursor.execute('SELECT * FROM admins WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if check_password(user['password_hash'], password):
        save_refresh_token_to_db(email)
        new_access_token = create_access_token(email, expiration_minutes=60) 
        return jsonify({'valid':True, 'message': 'Giriş başarılı.', 'token': new_access_token, 'user_type': user_type}), 200
    return jsonify({'valid':False, 'message': 'Şifreniz hatalıdır.'}), 401