import mysql.connector
import pandas as pd
import warnings

def load_data(host, user, password, database, query):
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
        return pd.DataFrame()

    # Tắt cảnh báo từ pandas
    warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy")

    # Đọc dữ liệu bằng pandas
    data = pd.read_sql(query, connection)

    connection.close()
    return data
