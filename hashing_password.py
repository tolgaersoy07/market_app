import bcrypt
def password_hashing(password:str)->str:
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

#check_password(Veritabanında ki şifre, Kullanıcının girdiği şifre)
def check_password(password_db:str,password_input:str)->bool:
    return bcrypt.checkpw(password_input.encode('utf-8'),password_db.encode('utf-8'))