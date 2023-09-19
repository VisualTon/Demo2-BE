from utils.utils_DB import get_addr_data_as_dict
from utils.utils_api import (
    create_connection,
)

if __name__ == "__main__":
    conn = create_connection()

    if conn:
        addr_data_dict = get_addr_data_as_dict(conn)
        print("Address Data as Dictionary:")
        print(addr_data_dict)
        check_addr = "0x123"
        print("test dict by input test addr 0x123: ")
        print(addr_data_dict.get(check_addr))
        # {'name': 'VisualTon', 'type': 'DEFI', 'url': 'https://www.google.com.tw/?hl=zh_TW'}
