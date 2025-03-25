from flask import Blueprint, jsonify,request,render_template
from hashing_password import password_hashing  
from token_services import get_email_from_token,create_access_token,save_refresh_token_to_db,get_user_type
from db import get_db_connection

user_info_bp = Blueprint('user_info', __name__)

@user_info_bp.route('/profile')
def profile():
    return render_template('profile.html')

@user_info_bp.route('/simple_user_info')
def user_info():
    token=request.headers.get('Authorization')
    email=get_email_from_token(token)
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute('SELECT first_name,last_name,balance FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_data = {"username": user["first_name"]+" "+user["last_name"],
        "balance": user["balance"]}
    return jsonify(user_data)

@user_info_bp.route('/user_profile', methods=['GET'])
def user_profile():
    token=request.headers.get('Authorization')
    email=get_email_from_token(token)
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute('SELECT first_name,last_name,phone,email,balance FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_data={"name":user["first_name"]+" "+user["last_name"].upper(),
                "phone":user["phone"],
                "email":user["email"],
                "balance":user["balance"]}
    return jsonify(user_data)

@user_info_bp.route('/change_email', methods=['POST'])
def change_email():
    access_token = request.headers.get('Authorization')
    data = request.get_json()
    new_email = data.get('email')
    old_email=get_email_from_token(access_token)
    if old_email==new_email:
        return jsonify({'error': 'Değiştireceğiniz E-Posta adresi aynı olamaz.'}), 400

    if not new_email:
        return jsonify({'error': 'Lütfen yeni E-Postanızı giriniz.'}), 400

    current_email = get_email_from_token(access_token)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Yeni e-posta başka bir kullanıcıya ait mi?
    cursor.execute('SELECT * FROM users WHERE email = %s', (new_email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Bu E-Posta başkası tarafından kullanılmaktadır.'}), 409

    # Kullanıcının e-postasını güncelle
    cursor.execute('UPDATE users SET email = %s WHERE email = %s', (new_email, current_email))
    conn.commit()

    cursor.close()
    conn.close()
    new_email_token=create_access_token(new_email)
    save_refresh_token_to_db(new_email)
    return jsonify({'message': 'Email updated successfully','token':new_email_token}), 200

@user_info_bp.route('/update_password', methods=['POST'])
def update_password():
    data = request.get_json()
    new_password = data.get('newPassword')
    new_password_repeat = data.get('confirmPassword')

    if new_password != new_password_repeat:
        return jsonify({'message': 'Şifreler eşleşmiyor!'}), 400
 
    # Şifreyi hash'le
    hashed_password = password_hashing(new_password)
    token=request.headers.get('Authorization')
    email=get_email_from_token(token)

    user_type=get_user_type(email)
    connect = get_db_connection()
    cursor = connect.cursor()
    if user_type=="user":
        cursor.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_password, email))
    elif user_type=="admin":
        cursor.execute("UPDATE admins SET password_hash = %s WHERE email = %s", (hashed_password, email))
    connect.commit()
    cursor.close()
    connect.close()
    return jsonify({'message': 'Şifreniz başarıyla güncellenmiştir.','code':200}), 200