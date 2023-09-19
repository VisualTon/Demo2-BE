import mysql.connector


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


def create_table(conn):
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE transactions (
        Transaction_id VARCHAR(255) NOT NULL,
        Block_id INT,
        Sender_address VARCHAR(255) NOT NULL,
        Receiver_address VARCHAR(255) NOT NULL,
        Type VARCHAR(255),
        Amount INT,
        Confirm_time INT
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'transactions' created successfully")


def create_addr_table(conn):
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS addresses (
        name VARCHAR(255),
        addr VARCHAR(255),
        type VARCHAR(255),
        url VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'addresses' created successfully")


if __name__ == "__main__":
    conn = create_connection()

    if conn:
        print("success connect")
        # create_table(conn)
        create_addr_table(conn)
        conn.close()
