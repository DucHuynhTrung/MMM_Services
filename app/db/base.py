import mysql.connector, os, asyncio
from typing import Type
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

async def execute_all_async[T](class_convert: Type[T], query: str, *params) -> list[T] | None:
    if query == '' or query == None:
        return None

    # Tạo đối tượng cursor để thực thi SQL
    loop = asyncio.get_event_loop()
    conn = conn_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    results = None

    try:
        cursor.execute(query, *params)        
        data = await loop.run_in_executor(None, cursor.fetchall)  # Thực thi câu truy vấn ở thread khác
        results = [class_convert(**row) for row in data] if data else None

    except mysql.connector.Error as err:
        print("Lỗi:", err)
        results = None
    finally:
        cursor.close()
        conn.close()

    return results


async def execute_one_async[T](class_convert: Type[T], query: str, *params) -> T | None:
    if query == '' or query == None:
        return None

    # Tạo đối tượng cursor để thực thi SQL
    loop = asyncio.get_event_loop()
    conn = conn_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    results = None

    try:
        cursor.execute(query, *params)        
        data = await loop.run_in_executor(None, cursor.fetchone)  # Thực thi câu truy vấn ở thread khác
        results = class_convert(**data) if data else None

    except mysql.connector.Error as err:
        print("Lỗi:", err)
        results = None
    finally:
        cursor.close()
        conn.close()

    return results


async def execute_none_async(query: str, *params) -> int | None:
    if query == '' or query == None:
        return None

    # Tạo đối tượng cursor để thực thi SQL
    loop = asyncio.get_event_loop()
    conn = conn_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    results = None

    try:
        def run() -> int:
            cursor.execute(query, *params)
            conn.commit()
            return cursor.rowcount

        # Chạy trong executor để tránh chặn async
        results = await loop.run_in_executor(None, run)

    except mysql.connector.Error as err:
        print("Lỗi:", err)
        results = None
    finally:
        cursor.close()
        conn.close()

    return results


async def put_queue_async[T](query: str, params: tuple = (), class_convert: Type[T] = int, fetch_one: bool = False) -> list[T] | dict[str, T] | T | None:
    future = asyncio.Future()
    """Thêm truy vấn vào queue để xử lý."""
    await query_queue.put((query, params, class_convert, fetch_one, future))

    if future is None:
        return None
    return await future


async def query_worker_async():
    """Worker chạy nền để xử lý query từ queue."""
    while True:
        query, params, class_convert, fetch_one, future = await query_queue.get()

        if query is None or query == '':
            continue

        results = None
        is_query_execute: bool = query.strip().upper().startswith(("SELECT", "EXEC"))
        is_query_execute_none: bool = not is_query_execute

        if (class_convert is int) and (is_query_execute_none):  # query Insert, Update or Delete
            results = await execute_none_async(query, params)
        elif (class_convert is not int) and (is_query_execute):  # query SELECT or EXEC
            if fetch_one:
                results = await execute_one_async(class_convert, query, params)
            else:
                results = await execute_all_async(class_convert, query, params)
        else:
            continue        # cần ghi log

        if future:  # Nếu có future (SELECT cần trả về dữ liệu)
            future.set_result(results)  # Gửi kết quả về future

        query_queue.task_done()


def start_query_workers(number_of_workers: int = 1):
    """Khởi tạo worker xử lý query."""
    for _ in range(number_of_workers):
        asyncio.create_task(query_worker_async())