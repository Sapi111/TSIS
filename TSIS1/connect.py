import psycopg2 #для постгре библиотека в питоне
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)# принимает значения словаря в конфиг.пу
