import mysql.connector
import pandas as pd
import warnings

# Tắt cảnh báo từ pandas
warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy")

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def insert_data(self, table_name, data):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()

            # Tạo bảng nếu chưa tồn tại
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_date DATETIME,
                city VARCHAR(100),
                product_id INT,
                quantity INT,
                sales FLOAT
            )
            """
            cursor.execute(create_table_query)

            # Chèn dữ liệu vào bảng
            insert_query = f"""
            INSERT INTO {table_name} (order_date, city, product_id, quantity, sales)
            VALUES (%s, %s, %s, %s, %s)
            """

            data_tuples = [
                (
                    row['order_date'], 
                    row['city'], 
                    int(row['product_id']), 
                    int(row['quantity']), 
                    float(row['sales'])
                ) 
                for _, row in data.iterrows()
            ]

            cursor.executemany(insert_query, data_tuples)
            connection.commit()
            print(f"Dữ liệu đã được lưu vào bảng {table_name}")
        except mysql.connector.Error as err:
            print(f"Lỗi khi lưu dữ liệu vào MySQL: {err}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def query(self, query):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            data = pd.read_sql(query, connection)
            connection.close()
            return data
        except mysql.connector.Error as err:
            print(f"Lỗi khi truy vấn dữ liệu từ MySQL: {err}")
            return pd.DataFrame()

    def read_query(self, query):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            data = pd.read_sql(query, connection)
            connection.close()
            return data  # Luôn trả về DataFrame
        except mysql.connector.Error as err:
            print(f"Lỗi khi truy vấn dữ liệu từ MySQL: {err}")
            return pd.DataFrame()  # Trả về DataFrame rỗng nếu có lỗi