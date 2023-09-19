from utils.utils_DB import add_data
from utils.utils_api import (
    tx,
    create_connection,
)

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
