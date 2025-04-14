# data__analysis.py
import pandas as pd

# Phân tích cho trường hợp chọn tháng và địa điểm
# data__analysis.py
def analyze_with_month_and_location(processed_data, month, year, location):
    # Tính toán doanh thu theo tháng và địa điểm
    monthly_sales = processed_data.groupby('Month')['sales'].sum().reset_index()

    month=int(month)
    total_sales_month = monthly_sales.loc[monthly_sales['Month'] == month, 'sales'].sum()

    if total_sales_month == 0:  # Kiểm tra nếu doanh thu là 0
        total_sales_month = "Không có doanh thu cho tháng này"

    # Tính toán ngày bán nhiều nhất trong tháng
    daily_sales = processed_data.groupby('Day')['sales'].sum().reset_index()
    best_day = daily_sales.loc[daily_sales['sales'].idxmax()]

    # Tính toán sản phẩm bán nhiều nhất
    top_products = processed_data.groupby('product_id')['quantity'].sum().reset_index()
    best_selling_product = top_products.loc[top_products['quantity'].idxmax()]

    product_name_map = {
        1: "Cà phê đen",
        2: "Cà phê sữa",
        3: "Bạc xỉu",
        4: "Capuchino",
        5: "Cà phê Chồn",
        6: "Socola cà phê",
        7: "Nước ngọt các loại",
        8: "Nước ép",
        9: "Sinh tố",
        10: "Tà sửa"
    }

    product_name = product_name_map.get(best_selling_product['product_id'], "Sản phẩm không xác định")

    result_text = f"Doanh thu tháng {month}/{year}: {int(total_sales_month)} VND\n"
    result_text += f"Ngày bán nhiều nhất: Ngày {int(best_day['Day'])} với doanh thu {int(best_day['sales'])} VND\n"
    result_text += f"Sản phẩm bán nhiều nhất: {product_name} với số lượng {int(best_selling_product['quantity'])} sản phẩm\n"

    return result_text, best_day, best_selling_product, daily_sales  # Chắc chắn rằng số giá trị trả về là 4


# Phân tích cho trường hợp chỉ chọn tháng
# data__analysis.py
# data__analysis.py
def analyze_with_month(processed_data, month, year):
    # Tính doanh thu theo tháng
    monthly_sales = processed_data.groupby('Month')['sales'].sum().reset_index()
    month=int(month)
    # Tìm doanh thu tháng đã chọn
    total_sales_month = monthly_sales.loc[monthly_sales['Month'] == month, 'sales'].sum()

    if total_sales_month == 0:  # Kiểm tra nếu doanh thu là 0
        total_sales_month = "Không có doanh thu cho tháng này"  # Không sử dụng int() nếu doanh thu là 0

    # Tính thành phố có doanh thu cao nhất trong tháng
    city_sales = processed_data.groupby('city')['sales'].sum().reset_index()
    best_city = city_sales.loc[city_sales['sales'].idxmax()]

    # Tính sản phẩm bán chạy nhất trong tháng
    top_products = processed_data.groupby('product_id')['quantity'].sum().reset_index()
    best_selling_product = top_products.loc[top_products['quantity'].idxmax()]

    product_name_map = {
        1: "Cà phê đen",
        2: "Cà phê sữa",
        3: "Bạc xỉu",
        4: "Capuchino",
        5: "Cà phê Chồn",
        6: "Socola cà phê",
        7: "Nước ngọt các loại",
        8: "Nước ép",
        9: "Sinh tố",
        10: "Tà sửa"
    }

    product_name = product_name_map.get(best_selling_product['product_id'], "Sản phẩm không xác định")

    # Tránh lỗi khi sử dụng int() trên chuỗi không phải là số
    try:
        result_text = f"Doanh thu tháng {month}/{year}: {int(total_sales_month)} VND\n"
    except ValueError:
        result_text = f"Doanh thu tháng {month}/{year}: {total_sales_month}\n"
    
    result_text += f"Thành phố có doanh thu cao nhất: {best_city['city']} với doanh thu {int(best_city['sales'])} VND\n"
    result_text += f"Sản phẩm bán chạy nhất: {product_name} với số lượng {int(best_selling_product['quantity'])} sản phẩm\n"

    return result_text, best_city, best_selling_product


# Phân tích cho trường hợp chỉ chọn địa điểm
def analyze_with_location(processed_data, location):
    # Tính doanh thu theo địa điểm
    location_sales = processed_data[processed_data['city'] == location].groupby('Month')['sales'].sum().reset_index()
    total_sales_location = location_sales['sales'].sum()

    # Tìm tháng có doanh thu cao nhất
    best_month = location_sales.loc[location_sales['sales'].idxmax()]

    # Tính sản phẩm bán chạy nhất theo địa điểm
    location_data = processed_data[processed_data['city'] == location]
    top_products = location_data.groupby('product_id')['quantity'].sum().reset_index()
    best_selling_product = top_products.loc[top_products['quantity'].idxmax()]

    product_name_map = {
        1: "Cà phê đen",
        2: "Cà phê sữa",
        3: "Bạc xỉu",
        4: "Capuchino",
        5: "Cà phê Chồn",
        6: "Socola cà phê",
        7: "Nước ngọt các loại",
        8: "Nước ép",
        9: "Sinh tố",
        10: "Tà sửa"
    }

    product_name = product_name_map.get(best_selling_product['product_id'], "Sản phẩm không xác định")

    result_text = f"Doanh thu tại {location}: {int(total_sales_location)} VND\n"
    result_text += f"Tháng có doanh thu cao nhất: Tháng {int(best_month['Month'])} với doanh thu {int(best_month['sales'])} VND\n"
    result_text += f"Sản phẩm bán chạy nhất tại {location}: {product_name} với số lượng {int(best_selling_product['quantity'])} sản phẩm\n"

    return result_text, best_month, best_selling_product

def analyze_data(data):
    monthly_sales = data.groupby(['Year', 'Month'])['sales'].sum().reset_index()
    best_month = monthly_sales.loc[monthly_sales['sales'].idxmax()]

    city_sales = data.groupby('city')['sales'].sum().reset_index()
    best_city = city_sales.loc[city_sales['sales'].idxmax()]

    hourly_sales = data.groupby('Hour')['sales'].sum().reset_index()

    top_products = data.groupby('product_id')['quantity'].sum().reset_index()
    best_selling_product = top_products.loc[top_products['quantity'].idxmax()]

    # Phân tích doanh thu theo ngày trong tháng
    daily_sales = data.groupby('Day')['sales'].sum().reset_index()

    result_text = f"Tháng có doanh thu cao nhất : Tháng {int(best_month['Month'])}/{int(best_month['Year'])} với doanh thu {int(best_month['sales'].round())}VND\n"
    result_text += f"Thành phố có doanh thu cao nhất : {best_city['city']} với doanh thu {int(best_city['sales'])}VND\n"
    result_text += f"Sản phẩm có doanh thu cao nhất : {best_selling_product['product_id']} với số lượng {best_selling_product['quantity']} sản phẩm "

    return result_text, hourly_sales, monthly_sales, daily_sales
# Thêm vào data__analysis.py
