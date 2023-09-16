import mysql.connector


class tx:
    tx_id: str
    block_id: int
    sender_address: str
    receiver_address: str
    type: str
    amount: int
    confirm_time: int


def create_connection():
    try:
        conn = mysql.connector.connect(
            host="3.112.222.156",
            port=3306,
            user="root",
            password="0505jo",
            database="example",
        )
        return conn
    except Exception as e:
        print(f"Error connecting to MySQL: {str(e)}")
        return None


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


if __name__ == "__main__":
    conn = create_connection()

    if conn:
        print("success connect")
        test_tx: tx = {
            "tx_id": "1",
            "block_id": 1,
            "sender_address": "1",
            "receiver_address": "1",
            "type": "",
            "amount": 1,
            "confirm_time": 1,
        }
        added_txs: [tx] = []
        added_txs.append(test_tx)
        add_data(conn, added_txs)

        conn.close()
