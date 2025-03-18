import mysql.connector
import pandas as pd

def load_data(host, user, password, database, query):
    # Kết nối đến cơ sở dữ liệu MySQL
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Kết nối thành công")
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối {err}")
    
    # Sử dụng pandas để đọc dữ liệu từ MySQL
    data = pd.read_sql(query, connection)
    
    # Đóng kết nối
    connection.close()
    
    return data
