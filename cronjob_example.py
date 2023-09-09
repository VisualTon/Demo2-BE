import schedule
import mysql.connector
import time


# 创建MySQL连接
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3390,
            user="root",
            password="0505jo",
            database="Example",
        )
        return conn
    except Exception as e:
        print(f"Error connecting to MySQL: {str(e)}")
        return None


def create_table(conn):
    # 创建游标对象
    cursor = conn.cursor()

    # 创建employees表
    create_table_query = """
    CREATE TABLE employees (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100),
        hire_date DATE
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'employees' created successfully")


# 新增记录
def add_employee(conn, employee_data):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO employees (employee_id, first_name, last_name, email, hire_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, employee_data)
        conn.commit()
        print("Employee added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error adding employee: {str(e)}")


# 编辑记录
def edit_employee(conn, employee_id, new_last_name):
    try:
        cursor = conn.cursor()
        sql = "UPDATE employees SET last_name = %s WHERE employee_id = %s"
        cursor.execute(sql, (new_last_name, employee_id))
        conn.commit()
        print("Employee edited successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error editing employee: {str(e)}")


# 删除记录
def delete_employee(conn, employee_id):
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM employees WHERE employee_id = %s"
        cursor.execute(sql, (employee_id,))
        conn.commit()
        print("Employee deleted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error deleting employee: {str(e)}")


# 定义要执行的任务函数
def my_job():
    conn = create_connection()

    if conn:
        # # 编辑员工记录
        edit_employee(conn, 1, str(int(time.time())))
        # 关闭数据库连接
        conn.close()


# 创建一个定期执行的任务，每小时执行一次
schedule.every().minute.do(my_job)

# 主循环，持续执行计划任务
while True:
    schedule.run_pending()
    time.sleep(1)  # 可以调整休眠时间以节省CPU资源
