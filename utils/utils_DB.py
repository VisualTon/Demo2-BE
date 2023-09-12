def add_data(conn, transaction_data):
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO transactions (Transaction_id, Block_id, Sender_address, Receiver_address, Type, Amount, Confirm_time)
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
        sql = "DELETE FROM transactions WHERE Transaction_id = %s"
        cursor.execute(sql, (transaction_id,))
        conn.commit()
        print(f"Data with Transaction_id '{transaction_id}' deleted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error deleting data: {str(e)}")


def print_table_data(conn):
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM transactions"
        cursor.execute(sql)

        # 获取所有数据行
        rows = cursor.fetchall()

        data_list = []

        # 将每行数据打包为 JSON 并添加到列表中
        for row in rows:
            (
                transaction_id,
                block_id,
                sender_address,
                receiver_address,
                type,
                amount,
                confirm_time,
            ) = row
            data = {
                "Transaction_id": transaction_id,
                "Block_id": block_id,
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
