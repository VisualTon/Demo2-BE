from utils.utils_DB import add_addr_data
from utils.utils_api import (
    tx,
    create_connection,
)

if __name__ == "__main__":
    conn = create_connection()

    if conn:
        print("success connect")
        add_addr_data(
            conn, "VisualTon", "0x123", "DEFI", "https://www.google.com.tw/?hl=zh_TW"
        )
        conn.close()
