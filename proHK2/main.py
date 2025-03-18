from src.data__load import load_data
from src.data__process import process_data
from src.data__analysis import analyze_data
from src.data__xili import visualize_data

def main():
    # Thông tin kết nối đến MySQL
    host = 'localhost'
    user = 'root'
    password = '24022005'
    database = 'doanhthubanhang'
    query = 'SELECT * FROM sales'  

    data = load_data(host, user, password, database, query)
    print("Dữ liệu đã tải:")
    print(data.head())

        # Xử lý dữ liệu
    processed_data = process_data(data)
    print("Dữ liệu đã xử lý:")
    print(processed_data.head())

        # Phân tích dữ liệu
    best_month, best_city, hourly_sales, best_selling_product = analyze_data(processed_data)

        # Trực quan hóa dữ liệu
    visualize_data(processed_data.groupby(['Year', 'Month'])['sales'].sum().reset_index(), hourly_sales)

        # Kết luận
    print(f"Doanh số tốt nhất là vào tháng {best_month['Month']} năm {best_month['Year']} với doanh số {best_month['sales']}.")
    print(f"Thành phố có doanh số cao nhất là {best_city['city']} với doanh số {best_city['sales']}.")
    print(f"Sản phẩm bán chạy nhất là {best_selling_product['product_id']} với số lượng {best_selling_product['quantity']}.")
       
    
   
if __name__=="__main__":
    main()