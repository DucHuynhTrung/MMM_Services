import mysql.connector, os, asyncio
from mysql.connector.pooling import MySQLConnectionPool
from dotenv import load_dotenv

load_dotenv()

config = {
    "host": os.getenv('HOST'),
    "user": os.getenv('USER'),
    "password": os.getenv('PASS'),
    "database": os.getenv('DATABASE')
}

conn_pool = MySQLConnectionPool(pool_name="my_connection_pool", pool_size=5, pool_reset_session=True, **config)

query_queue = asyncio.Queue()

async def execute_query(query: str, params:tuple=(), class_convert=None, fetch_one:bool=False, fetch_all:bool=True, as_dict:bool=False):
    if query == '' or query == None:
        return None

    # Tạo đối tượng cursor để thực thi SQL
    loop = asyncio.get_event_loop()
    conn = conn_pool.get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        
        # Nếu là SELECT hoặc PROCEDURE
        if query.strip().upper().startswith(("SELECT", "EXEC")):
            results = await loop.run_in_executor(None, cursor.fetchall if fetch_all else cursor.fetchone)  # Thực thi câu truy vấn ở thread khác

            # Chuyển đổi thành object nếu có class
            if class_convert and results:
                if fetch_one:
                    results = class_convert(**results) if results else None
                elif as_dict:
                    results = {next(iter(row.values())): class_convert(**row) for row in results} if results else None
                else:
                    results = [class_convert(**row) for row in results] if results else None        # next(iter(row.values())): chuyển giá trị dict thành list rồi lấy giá trị đầu tiên mà không cần quan tâm tên cột

        else:  # Nếu là INSERT, UPDATE, DELETE
            conn.commit()
            results = cursor.rowcount  # Trả về số dòng bị ảnh hưởng

    except mysql.connector.Error as err:
        print("Lỗi:", err)
        results = None
    finally:
        cursor.close()
        conn.close()

    return results


async def add_to_queue(query, params:tuple=(), class_convert=None, fetch_one:bool=False, fetch_all:bool=True, as_dict:bool=False, return_result:bool=False) -> asyncio.Future | None:
    future = asyncio.Future() if return_result else None  # Tạo future nếu cần kết quả
    """Thêm truy vấn vào queue để xử lý."""
    await query_queue.put((query, params, class_convert, fetch_one, fetch_all, as_dict, future))

    if return_result and future != None:  # Nếu cần kết quả, đợi future hoàn thành
        return await future


async def query_worker():
    """Worker chạy nền để xử lý query từ queue."""
    while True:
        query, params, class_convert, fetch_one, fetch_all, as_dict, future = await query_queue.get()
        results = await execute_query(query, params, class_convert, fetch_one, fetch_all, as_dict)

        if future:  # Nếu có future (SELECT cần trả về dữ liệu)
            future.set_result(results)  # Gửi kết quả về future

        query_queue.task_done()


def start_query_workers(number_of_workers: int = 1):
    """Khởi tạo worker xử lý query."""
    for _ in range(number_of_workers):
        asyncio.create_task(query_worker())