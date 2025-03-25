import jwt
from config import SECRET_KEY
from token_encryption import encrypt_token,decrypt_token
from db import get_db_connection
from datetime import datetime, timedelta, timezone
from flask import request

def get_user_type(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM admins WHERE email = %s", (email,))
    is_admin = cursor.fetchone()
    if is_admin:
        return "admin"
    cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
    is_user = cursor.fetchone()
    if is_user:
        return "user"
    conn.close()
    return "no_one"

# Access token'ı oluşturma fonksiyonu
def create_access_token(email: str, expiration_minutes: int = 60):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    device_id = request.cookies.get('deviceID_marketapp')
    payload = {
        'email': email,
        'exp': expiration_time,
        'device_id': device_id,
        'user_type': get_user_type(email)
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return access_token

# Refresh token'ı oluşturma fonksiyonu
def create_refresh_token(email: str):
    expiration_time = datetime.now(timezone.utc) + timedelta(days=30)  # 30 gün
    new_expiration_time = expiration_time.replace(hour=4, minute=0, second=0, microsecond=0)
    device_id = request.cookies.get('deviceID_marketapp')
    payload = {
        'email': email,
        'exp': new_expiration_time,
        'device_id': device_id,
        'user_type': get_user_type(email)
    }
    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return refresh_token

# Refresh token'ı veritabanına kaydetme
def save_refresh_token_to_db(email: str):
    refresh_token=create_refresh_token(email)
    encrypted_token = encrypt_token(refresh_token)  # Refresh token'ı şifrele
    conn = get_db_connection()
    cursor = conn.cursor()

    # Email'e göre var mı kontrol et.
    # Bu güncelleme sayesinde oturum sadece en yeni giriş yapmış cihazda kalır.
    # Diğerlerinden de çıkış yapılmış olur.
    cursor.execute("SELECT COUNT(*) FROM refresh_tokens WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result[0]>0:  # Eğer email zaten varsa, refresh token'ı güncelle
        cursor.execute("UPDATE refresh_tokens SET refresh_token = %s WHERE email = %s", 
            (encrypted_token, email))
    else: # Eğer yoksa, yeni bir kayıt oluştur
        cursor.execute("INSERT INTO refresh_tokens (refresh_token, email) VALUES (%s, %s)", 
            (encrypted_token, email))
    conn.commit() 
    conn.close() 

def get_email_from_token(token):
    try:
        return jwt.decode(token[7:],SECRET_KEY,algorithms=['HS256'],options={"verify_exp":False}).get('email')
    except jwt.InvalidTokenError:
        return None
        
def token_control():
    device_id = request.cookies.get('deviceID_marketapp')
    print("device_id token control:",device_id,type(device_id))
    if not device_id:
        return {'valid': False, 'code': 401, 'error_code': 'NO_DEVICE_ID'}
    
    token = request.headers.get('Authorization')
    if token == "Bearer " or not token:
        args_token = request.args.get('token')
        if not args_token:
            return {'valid': False, 'code': 401, 'error_code': 'NO_TOKEN'}
        token=args_token

    if not token:
        return {'valid': False, 'code': 401, 'error_code':
            'NO_TOKEN', 'message': 'Authorization token is missing'}

    if token.startswith("Bearer "):
        token = token[7:]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})

        # Device ID doğrulama
        if device_id != payload['device_id']:
            return {'valid': False, 'code': 401, 'error_code': 'INVALID_DEVICE_ID'}
        
        result=verify_refresh_token(payload['email'])

        # Token expiration kontrolü
        if datetime.fromtimestamp(payload['exp'], timezone.utc) < datetime.now(timezone.utc):
            if result['code']==200:
                new_access_token = create_access_token(payload['email'])
                return {'token':new_access_token, 'valid': True, 'code': 200, 
                    'error_code': 'VALID_TOKEN', 'user_type': payload['user_type']}
            return {'valid': False, 'code': 401, 'error_code': 'REFRESH_TOKEN_EXPIRED'}
        if result['valid']==False:
            return {'valid': False, 'code': 401, 'error_code': 'REFRESH_TOKEN_EXPIRED'}   
        return {'token':token, 'valid': True, 'code': 200, 'error_code': 'VALID_TOKEN', 'user_type': payload['user_type']}

    except jwt.DecodeError:
        return {'valid': False, 'code': 401, 'error_code': 'INVALID_TOKEN'}
    except Exception as e:
        # Diğer hataları yakalamak için genel bir except bloğu
        print("token_control() error:", str(e))
        return {'valid': False, 'code': 400, 'error_code': 'ERROR', 'message': str(e)}

def verify_refresh_token(email):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT refresh_token FROM refresh_tokens WHERE email=%s", (email,))
        result=cursor.fetchone()
        conn.close()

        if not result:
            return {'valid': False, 'code': 403, 'error_code': 'NO_REFRESH_TOKEN'}

        refresh_token = decrypt_token(result[0])

        try:
            payload=jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            if payload['device_id'] != request.cookies.get('deviceID_marketapp'):
                return {'valid': False, 'code': 401, 'error_code': 'INVALID_DEVICE_ID'}
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'code': 401, 'error_code': 'REFRESH_TOKEN_EXPIRED'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'code': 401, 'error_code': 'INVALID_TOKEN'}

        return {'valid': True, 'code': 200, 'error_code': 'VALID_TOKEN'}
    
    except Exception as e:
        return {'valid': False, 'code': 500, 'error_code': 'SERVER_ERROR', 'message': str(e)}

def create_reset_password_token(email: str, phone: str, expiration_minutes: int = 500):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    device_id = request.cookies.get('deviceID_marketapp')
    payload = {
        'email': email,
        'phone': phone,
        'exp': expiration_time,
        'device_id': device_id
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return access_token

def decode_reset_password_token(reset_token: str):
    try:
        decoded_token = jwt.decode(reset_token, SECRET_KEY, algorithms=['HS256'])
        email = decoded_token.get('email')
        phone = decoded_token.get('phone')
        return [email, phone]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
