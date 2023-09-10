import mysql.connector
import time
import json


# 创建MySQL连接
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3390,
            user="root",
            password="0505jo",
            database="Example",
        )
        return conn
    except Exception as e:
        print(f"Error connecting to MySQL: {str(e)}")
        return None


def create_table(conn):
    # 创建游标对象
    cursor = conn.cursor()

    # 创建employees表
    create_table_query = """
    CREATE TABLE transactions2 (
        Transaction_id VARCHAR(255) NOT NULL,
        Sender_address VARCHAR(255) NOT NULL,
        Receiver_address VARCHAR(255) NOT NULL,
        Type VARCHAR(255),
        Amount INT,
        Confirm_time INT
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'employees' created successfully")


def add_data(conn, transaction_data):
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO transactions2 (Transaction_id, Sender_address, Receiver_address, Type, Amount, Confirm_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, transaction_data)
        conn.commit()
        print("Data added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error adding data: {str(e)}")


# 删除特定数据（根据Transaction_id）
def delete_data(conn, transaction_id):
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM transactions2 WHERE Transaction_id = %s"
        cursor.execute(sql, (transaction_id,))
        conn.commit()
        print(f"Data with Transaction_id '{transaction_id}' deleted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error deleting data: {str(e)}")


def print_table_data(conn):
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM transactions2"
        cursor.execute(sql)

        # 获取所有数据行
        rows = cursor.fetchall()

        data_list = []

        # 将每行数据打包为 JSON 并添加到列表中
        for row in rows:
            (
                transaction_id,
                sender_address,
                receiver_address,
                type,
                amount,
                confirm_time,
            ) = row
            data = {
                "Transaction_id": transaction_id,
                "Sender_address": sender_address,
                "Receiver_address": receiver_address,
                "Type": type,
                "Amount": amount,
                "Confirm_time": confirm_time,
            }
            data_list.append(data)

        # 将数据列表转换为 JSON 格式并打印
        print(data_list)

    except Exception as e:
        print(f"Error fetching data: {str(e)}")


if __name__ == "__main__":
    # 连接到MySQL数据库
    conn = create_connection()

    if conn:
        print("success connect")
        # 創建表格
        # create_table(conn)

        # 添加新数据
        transaction_data = (
            str(int(time.time())),
            "Sender_Address",
            "Receiver_Address",
            "DEFI",
            100,
            int(time.time()),
        )
        add_data(conn, transaction_data)

        # # 删除特定数据（根据Transaction_id）
        # transaction_id_to_delete = "New_Transaction_ID"
        # delete_data(conn, transaction_id_to_delete)

        print_table_data(conn)
        # 关闭数据库连接
        conn.close()
