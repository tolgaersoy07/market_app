from cryptography.fernet import Fernet
import base64
from config import FERNET_ENCRYPTION_KEY
key_bytes = FERNET_ENCRYPTION_KEY.encode('utf-8')

# Anahtar oluşturma
def generate_key():
    result=Fernet.generate_key()
    key_string=result.decode('utf-8')
    return key_string

# Şifreleme işlemi
def encrypt_token(data: str) -> str:
    key=key_bytes
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())  # Veriyi şifrele
    return encrypted_data.decode()  # Şifrelenmiş veriyi döndür

# Şifreyi çözme işlemi
def decrypt_token(encrypted_data: str) -> str:
    key=key_bytes
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode())  # Şifreyi çöz
    return decrypted_data.decode()  # Çözülen veriyi döndür