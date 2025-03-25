import mysql.connector
from config import db_info 

def get_db_connection():
    return mysql.connector.connect(
        host=db_info['host'],      
        user=db_info['user'],           
        password=db_info['password'],   
        database=db_info['database']
        )