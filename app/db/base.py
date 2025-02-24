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


def select(query: str, params:tuple=(), class_convert=None) -> dict:
    # Tạo đối tượng cursor để thực thi SQL
    conn = connect()
    cursor = conn.cursor(dictionary=True)

    # Thực thi truy vấn
    cursor.execute(query, params)
    datas = cursor.fetchall()

    results = {}
    if class_convert:
        results = {result["ID"]: class_convert(**result) for result in datas}

    # Đóng kết nối
    cursor.close()
    conn.close()
    return results
