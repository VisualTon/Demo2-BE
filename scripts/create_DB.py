import mysql.connector
import time
import json


# 创建MySQL连接
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # 如果 MySQL 服务器在本地，使用 "localhost"；如果在不同的主机上，使用该主机的 IP 地址
            port=3390,  # 映射的本地端口
            user="root",  # MySQL 用户名
            password="0505jo",  # MySQL 密码
            database="visualtondb",  # 要连接的数据库名称
        )
        return conn
    except Exception as e:
        print(f"Error connecting to MySQL: {str(e)}")
        return None


def create_table(conn):
    # 创建游标对象
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE transactions (
        Transaction_id VARCHAR(255) NOT NULL,
        Block_id INT,
        Sender_address VARCHAR(255) NOT NULL,
        Receiver_address VARCHAR(255) NOT NULL,
        Type VARCHAR(255),
        Amount INT,
        Confirm_time INT
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'transactions' created successfully")


if __name__ == "__main__":
    # 连接到MySQL数据库
    conn = create_connection()

    if conn:
        print("success connect")
        # 創建表格
        create_table(conn)
        conn.close()
