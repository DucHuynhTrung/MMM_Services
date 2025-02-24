import mysql.connector

def connect():
    return mysql.connector.connect(
        host="45.252.251.51",
        user="ivizdbhn_sa",
        password="TrungDuc1231998",
        database="ivizdbhn_MMM"
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
