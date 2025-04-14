import pandas as pd

def process_data(data):
    try:
        # Chuyển đổi 'order_date' thành định dạng datetime và xử lý các lỗi
        data['Order Date'] = pd.to_datetime(data['order_date'], errors='coerce')
        print("Dữ liệu sau khi chuyển đổi ngày tháng:", data.head())  # In ra một vài dòng đầu để kiểm tra

        # Loại bỏ các dòng có giá trị ngày tháng không hợp lệ
        data = data.dropna(subset=['Order Date'])
        print("Dữ liệu sau khi loại bỏ các dòng có ngày tháng không hợp lệ:", data.head())

        # Kiểm tra các cột cần thiết
        required_columns = ['order_date', 'city', 'product_id', 'quantity', 'sales']
        if not all(col in data.columns for col in required_columns):
            raise ValueError("Dữ liệu thiếu các cột cần thiết!")

        # Loại bỏ các dòng có dữ liệu thiếu ở các cột quan trọng khác
        data = data.dropna(subset=['city', 'product_id', 'quantity', 'sales'])
        print("Dữ liệu sau khi loại bỏ các dòng thiếu giá trị quan trọng:", data.head())

        # Loại bỏ các dòng trùng lặp
        data = data.drop_duplicates()
        print("Dữ liệu sau khi loại bỏ các dòng trùng lặp:", data.head())

        # Kiểm tra và xử lý các giá trị bất hợp lệ:
        # Kiểm tra các giá trị âm trong 'sales' và 'quantity', vì chúng không hợp lệ trong bối cảnh này
        data = data[data['sales'] >= 0]
        data = data[data['quantity'] >= 0]

        # Thêm các cột cho tháng, năm, giờ và ngày
        data['Month'] = data['Order Date'].dt.month
        data['Year'] = data['Order Date'].dt.year
        data['Hour'] = data['Order Date'].dt.hour
        data['Day'] = data['Order Date'].dt.day  # Thêm cột Day cho ngày trong tháng

        print("Dữ liệu sau khi thêm các cột tháng, năm, giờ, ngày:", data.head())

        # Loại bỏ các dòng có dữ liệu thiếu sau khi xử lý
        data = data.dropna()
        print("Dữ liệu sau khi loại bỏ các dòng có dữ liệu thiếu sau xử lý:", data.head())

        return data

    except Exception as e:
        print("Lỗi trong quá trình xử lý dữ liệu:", e)
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu có lỗi
