# db.py
import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

POOL = pooling.MySQLConnectionPool(
    pool_name="mb_pool",
    pool_size=5,
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "moffatbay"),
    auth_plugin='mysql_native_password'  # helps if your server uses native auth
)

def get_conn():
    return POOL.get_connection()
