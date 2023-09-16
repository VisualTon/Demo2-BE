class tx:
    tx_id: str
    block_id: int
    sender_address: str
    receiver_address: str
    type: str
    amount: int
    confirm_time: int


def add_data(conn, transaction_data):
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO transactions (Transaction_id, Block_id, Sender_address, Receiver_address, Type, Amount, Confirm_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for tx in transaction_data:
            data = (
                tx["tx_id"],
                tx["block_id"],
                tx["sender_address"],
                tx["receiver_address"],
                tx["type"],
                (int(tx["amount"]) / 1000000000),
                tx["confirm_time"],
            )
            cursor.execute(sql, data)

        conn.commit()
        print("Data added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error adding data: {str(e)}")


def delete_data(conn, block_ids: [int]):
    for block_id in block_ids:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM transactions WHERE Block_id = %s"
            cursor.execute(sql, (block_id,))
            conn.commit()
            # print(f"Data with Block_id '{block_id}' deleted successfully")
        except Exception as e:
            conn.rollback()
            print(f"Error deleting data: {str(e)}")


def delete_duplicate_data(txs: [tx]) -> [tx]:
    seen = set()
    result: [tx] = []

    for item in txs:
        record = (
            item["block_id"],
            item["sender_address"],
            item["receiver_address"],
            item["amount"],
            item["confirm_time"],
        )

        if record not in seen:
            seen.add(record)
            result.append(item)

    return result


def get_table_data(conn) -> [tx]:
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM transactions"
        cursor.execute(sql)

        rows = cursor.fetchall()

        data_list: [tx] = []

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
            data: tx = {
                "Transaction_id": transaction_id,
                "Block_id": block_id,
                "Sender_address": sender_address,
                "Receiver_address": receiver_address,
                "Type": type,
                "Amount": amount,
                "Confirm_time": confirm_time,
            }
            data_list.append(data)

        return data_list

    except Exception as e:
        print(f"Error fetching data: {str(e)}")
