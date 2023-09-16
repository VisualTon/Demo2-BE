from utils.utils_DB import delete_data
from utils.utils_api import (
    create_connection,
)


class tx:
    tx_id: str
    block_id: int
    sender_address: str
    receiver_address: str
    type: str
    amount: int
    confirm_time: int


if __name__ == "__main__":
    conn = create_connection()

    if conn:
        print("success connect")
        remove_id = 1
        removed_block_ids: [int] = []
        removed_block_ids.append(remove_id)
        delete_data(conn, removed_block_ids)

        conn.close()
