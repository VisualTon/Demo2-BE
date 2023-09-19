from utils.utils_api import (
    tx,
    create_connection,
)


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


if __name__ == "__main__":
    conn = create_connection()

    if conn:
        print("success connect")
        all_txs: [tx] = get_table_data(conn)
        print(f"there are {len(all_txs)} txs in table.")

        conn.close()
