import mysql.connector
from utils.utils_DB import get_addr_data_as_dict


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


if __name__ == "__main__":
    conn = create_connection()

    if conn:
        addr_data_dict = get_addr_data_as_dict(conn)
        print("Address Data as Dictionary:")
        print(addr_data_dict)
        check_addr = "0x123"
        print("test dict by input test addr 0x123: ")
        print(addr_data_dict.get(check_addr))
