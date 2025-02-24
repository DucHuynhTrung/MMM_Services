import mysql.connector, os
from dotenv import load_dotenv

load_dotenv()

def connect():
    host = os.getenv('HOST')
    user = os.getenv('USER')
    password = os.getenv('PASS')
    database = os.getenv('DATABASE')

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def select(query: str):
    # Tạo đối tượng cursor để thực thi SQL
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    # Thực thi truy vấn
    cursor.execute(query)
    result = cursor.fetchone()

    # Đóng kết nối
    cursor.close()
    conn.close()
    return f"Đang kết nối đến DB: {result}"
