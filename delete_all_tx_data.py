from utils.utils_api import (
    create_connection,
)

if __name__ == "__main__":
    conn = create_connection()

    if conn:
        cursor = conn.cursor()

        sql = "DELETE FROM transactions"

        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
