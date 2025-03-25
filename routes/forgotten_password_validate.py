from flask import Blueprint, request, jsonify,render_template
from db import get_db_connection  
from hashing_password import password_hashing  
from token_services import get_user_type,create_reset_password_token,decode_reset_password_token

forgotten_password_validate_bp = Blueprint('forgotten_password_validate', __name__)

@forgotten_password_validate_bp.route('/forgotten_password')
def forgotten_password():
    return render_template('forgetted_password.html')

@forgotten_password_validate_bp.route('/forgotten_password_validate', methods=['POST'])
def forgotten_password_validate():
    data = request.get_json()
    email = data.get('email')
    phone = data.get('phone')
    
    if not email or not phone:
        return jsonify({'message': 'E-posta ve telefon numarası gereklidir!'}), 400

    # Veritabanı bağlantısını kur
    connect = get_db_connection()
    cursor = connect.cursor(dictionary=True)

    # Kullanıcıyı doğrulamak için SQL sorgusu
    cursor.execute('SELECT * FROM users WHERE email = %s AND phone = %s', (email, phone))
    user = cursor.fetchone()
    if not user:
        cursor.execute('SELECT * FROM admins WHERE email = %s AND phone = %s', (email, phone))
        user = cursor.fetchone()
    cursor.close()
    connect.close()
    if user:
        token=create_reset_password_token(email,phone)
        return jsonify({'message': 'Şifrenizi sıfırlayabilirsiniz.','code':200, 'token':token}), 200

    return jsonify({'message': 'Böyle bir kullanıcı bulunamadı!'}), 404



@forgotten_password_validate_bp.route('/reset_password', methods=['POST'])
def reset_password():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token gereklidir!'}), 400
    result=decode_reset_password_token(token[7:])
    if not result:
        return jsonify({'message': 'Token geçersiz!'}), 401
    email=result[0]
    phone=result[1]

    data = request.get_json()
    new_password = data.get('newPassword')
    new_password_repeat = data.get('confirmPassword')

    if not email or not phone or not new_password:
        return jsonify({'message': 'Veriler boş olamaz!'}), 400

    if new_password != new_password_repeat:
        return jsonify({'message': 'Şifreler eşleşmiyor!'}), 400
 
    # Şifreyi hash'le
    hashed_password = password_hashing(new_password)

    user_type=get_user_type(email)
    connect = get_db_connection()
    cursor = connect.cursor()
    if user_type=="user":
        cursor.execute("UPDATE users SET password_hash = %s WHERE email = %s AND phone = %s", (hashed_password, email, phone))
    elif user_type=="admin":
        cursor.execute("UPDATE admins SET password_hash = %s WHERE email = %s AND phone = %s", (hashed_password, email, phone))
    if user_type!="no_one":
        cursor.execute("DELETE FROM refresh_tokens WHERE email=%s", (email,))
    connect.commit()
    cursor.close()
    connect.close()
    return jsonify({'message': 'Şifreniz başarıyla güncellenmiştir.','code':200}), 200

