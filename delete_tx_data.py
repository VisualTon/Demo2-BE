from utils.utils_DB import delete_data
from utils.utils_api import (
    create_connection,
)

if __name__ == "__main__":
    conn = create_connection()

    if conn:
        print("success connect")
        remove_id = 1
        removed_block_ids: [int] = []
        removed_block_ids.append(remove_id)
        delete_data(conn, removed_block_ids)

        conn.close()
