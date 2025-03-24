import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from src.data__load import load_data
from src.data__process import process_data
from src.data__analysis import analyze_data
from src.database import Database
from src.config import db_config

def run_analysis(selected_year):
    global result_label  # Thêm dòng này để đảm bảo biến được nhận diện trong hàm
    import pandas as pd

    # Kết nối tới cơ sở dữ liệu
    db = Database(**db_config)
    query = f"SELECT * FROM doanhthu{selected_year}"

    data = db.query(query)
    if data.empty:
        result_label.config(text=f"Dữ liệu năm {selected_year} không tồn tại hoặc rỗng.")
        return  # Thoát khỏi hàm nếu dữ liệu rỗng

    # Xử lý dữ liệu
    processed_data = process_data(data)

    # Phân tích dữ liệu
    best_month, best_city, hourly_sales, best_selling_product = analyze_data(processed_data)

    # Hiển thị kết quả phân tích
    result_text = (
        f"Doanh số tốt nhất là vào tháng {best_month['Month']} năm {best_month['Year']} với doanh số {best_month['sales']}.\n"
        f"Thành phố có doanh số cao nhất là {best_city['city']} với doanh số {best_city['sales']}.\n"
        f"Sản phẩm bán chạy nhất là {best_selling_product['product_id']} với số lượng {best_selling_product['quantity']}."
    )
    result_label.config(text=result_text)

    # Vẽ biểu đồ
    plot_data(processed_data.groupby(['Year', 'Month'])['sales'].sum().reset_index(), hourly_sales)


def plot_data(monthly_sales, hourly_sales):
    # Xóa canvas cũ (nếu có)
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Tạo figure mới
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Biểu đồ 1 - Doanh số theo tháng
    axes[0].plot(monthly_sales['Month'], monthly_sales['sales'], marker='o')
    axes[0].set_title('Doanh số theo tháng')
    axes[0].set_xlabel('Tháng')
    axes[0].set_ylabel('Doanh số')
    axes[0].grid(True)

    # Biểu đồ 2 - Doanh số theo giờ
    axes[1].bar(hourly_sales['Hour'], hourly_sales['sales'])
    axes[1].set_title('Doanh số theo giờ')
    axes[1].set_xlabel('Giờ trong ngày')
    axes[1].set_ylabel('Doanh số')
    axes[1].grid(True)

    # Nhúng biểu đồ vào Tkinter
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Tạo giao diện bằng Tkinter
root = tk.Tk()
root.title("Phân tích doanh thu bán hàng")

# Layout giao diện dạng lưới
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# Thanh chọn năm
year_label = tk.Label(root, text="Chọn năm:")
year_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)

year_options = ['2021', '2022', '2023', '2024', '2025']
selected_year = ttk.Combobox(root, values=year_options, state="readonly")
selected_year.set("2021")
selected_year.grid(row=0, column=1, sticky='w', padx=10, pady=5)

# Nút chạy phân tích
analyze_button = tk.Button(root, text="Phân tích", command=lambda: run_analysis(selected_year.get()))
analyze_button.grid(row=1, column=0, columnspan=2, pady=10)

# Khung chứa kết quả
result_label = tk.Label(root, text="", wraplength=400, justify="left")
result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Khung chứa biểu đồ
canvas_frame = tk.Frame(root)
canvas_frame.grid(row=3, column=0, columnspan=2, pady=10)

# Hiển thị biểu đồ ngay khi mở giao diện
run_analysis(selected_year.get())

root.mainloop()
