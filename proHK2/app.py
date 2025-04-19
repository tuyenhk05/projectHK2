import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker  # Đảm bảo bạn đã nhập thư viện ticker

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.excel_import import import_excel
from src.data__process import process_data
from src.data__analysis import analyze_data, forecast_sales_arima
from src.database import Database
from src.config import db_config
from src.data__analysis import analyze_with_month_and_location, analyze_with_month, analyze_with_location

# Kết nối database
db = Database(**db_config)

# Hàm vẽ biểu đồ
# Hàm vẽ biểu đồ
def visualize_data(monthly_sales, hourly_sales, daily_sales, canvas_frame):
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Doanh số theo tháng
    if not monthly_sales.empty:
        axes[0].plot(monthly_sales['Month'], monthly_sales['sales'], marker='o')
        axes[0].set_title('Doanh số theo tháng')
        axes[0].set_xticks(range(1, 13))
        axes[0].grid(True)

        # Định dạng trục y và giảm kích thước font để không bị đè lên
        axes[0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        axes[0].tick_params(axis='y', labelsize=6)  # Giảm kích thước font của trục y

    # Doanh số theo ngày
    if not daily_sales.empty and 'Day' in daily_sales.columns:
        axes[1].plot(daily_sales['Day'], daily_sales['sales'], marker='o', color='green')
        axes[1].set_title('Doanh số theo ngày trong tháng')
        axes[1].set_xticks(range(1, 32, 3))  # Cách 3 ngày để dễ nhìn hơn
        axes[1].grid(True)

        # Định dạng trục y và giảm kích thước font
        axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        axes[1].tick_params(axis='y', labelsize=6)  # Giảm kích thước font của trục y

    # Doanh số theo giờ
    if not hourly_sales.empty:
        axes[2].bar(hourly_sales['Hour'], hourly_sales['sales'])
        axes[2].set_title('Doanh số theo giờ')
        axes[2].set_xticks(range(0, 24, 2))  # Hiển thị theo giờ cách 2 tiếng
        axes[2].grid(True)

        # Định dạng trục y và giảm kích thước font
        axes[2].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        axes[2].tick_params(axis='y', labelsize=6)  # Giảm kích thước font của trục y

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Nhập & lưu dữ liệu đã làm sạch
def import_and_save_data():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if not file_path:
        return

    raw_data = import_excel(file_path)
    if raw_data.empty:
        messagebox.showerror("Lỗi", "File Excel trống hoặc sai định dạng.")
        return

    try:
        cleaned_data = process_data(raw_data)
    except Exception as e:
        messagebox.showerror("Lỗi xử lý", f"{e}")
        return

    if cleaned_data.empty:
        messagebox.showerror("Lỗi", "Dữ liệu sau xử lý trống.")
        return

    try:
        db.insert_data("doanhthu_excel", cleaned_data)
        messagebox.showinfo("Thành công", "Dữ liệu đã lưu vào MySQL!")
    except Exception as e:
        messagebox.showerror("Lỗi MySQL", f"{e}")

# Phân tích & hiển thị
def run_analysis():
    forecast_canvas_frame.pack_forget()  # Ẩn khung dự báo nếu đang hiện
    canvas_frame.pack(pady=10)
    year = selected_year.get()
    month = selected_month.get()
    location = selected_location.get()

    # Cập nhật truy vấn SQL dựa trên việc chọn tháng và địa điểm
    query = f"SELECT * FROM doanhthu_excel WHERE YEAR(order_date) = {year}"

    # Thêm điều kiện tháng nếu có
    if month:
        query += f" AND MONTH(DATE(order_date)) = {month}"

    # Thêm điều kiện địa điểm nếu có
    if location:
        query += f" AND city = '{location}'"

    # Debug: In ra truy vấn SQL để kiểm tra
    print("Truy vấn SQL:", query)

    try:
        data = db.read_query(query)
    except Exception as e:
        result_label.config(text=f"Lỗi truy vấn: {e}")
        return

    if data.empty:
        result_label.config(text="Không có dữ liệu phù hợp.")
        return

    try:
        processed = process_data(data)
        result_text, hourly_sales, monthly_sales, daily_sales = analyze_data(processed)
        result_label.config(text=result_text)

        visualize_data(monthly_sales, hourly_sales, daily_sales, canvas_frame)
        # Trường hợp chọn cả tháng và địa điểm
        if month and location:
            result_text, best_day, best_selling_product, daily_sales = analyze_with_month_and_location(processed, month, year, location)
            result_label.config(text=result_text)

        # Trường hợp chỉ chọn tháng
        elif month:
            result_text, best_city, best_selling_product = analyze_with_month(processed, month, year)
            result_label.config(text=result_text)

        # Trường hợp chỉ chọn địa điểm
        elif location:
            result_text, best_month, best_selling_product = analyze_with_location(processed, location)
            result_label.config(text=result_text)

        
            # Phân tích bình thường khi không chọn tháng và địa điểm
            

    except Exception as e:
        result_label.config(text=f"Lỗi phân tích: {e}")
def run_sales_forecast():
    try:
        data = db.read_query("SELECT * FROM doanhthu_excel")
        if data.empty:
            result_label.config(text="Không có dữ liệu để dự báo.")
            return

        data['order_date'] = pd.to_datetime(data['order_date'], errors='coerce')
        data.dropna(subset=['order_date'], inplace=True)

        # 1. Ẩn biểu đồ phân tích nếu đang hiện
        canvas_frame.pack_forget()

        # 2. Xóa khung biểu đồ dự báo (nếu có cũ)
        clear_forecast_canvas()

        # 3. Hiện lại frame dự báo
        forecast_canvas_frame.pack(pady=10)

        # 4. Gọi hàm dự báo & vẽ
        fig = forecast_sales_arima(data)

        canvas = FigureCanvasTkAgg(fig, master=forecast_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        result_label.config(text="Dự báo doanh thu đã được hiển thị.")
    except Exception as e:
        result_label.config(text=f"Lỗi trong quá trình dự báo: {e}")

def compare_by_year_month_location():
    year = selected_year.get()
    compare_year = selected_year_compare.get()  # Năm so sánh
    month = selected_month.get()
    compare_month = selected_month_compare.get()  # Tháng so sánh
    location = selected_location.get()

    # Xóa biểu đồ cũ trước khi vẽ lại
    clear_canvas()

    # Trường hợp người dùng chỉ chọn năm (so sánh giữa 2 năm)
    if not month and not compare_month:
        # Xây dựng truy vấn SQL cho năm hiện tại
        query_current = f"SELECT * FROM doanhthu_excel WHERE YEAR(order_date) = {year}"
        if location:
            query_current += f" AND city = '{location}'"

        # Xây dựng truy vấn SQL cho năm so sánh
        query_compare = f"SELECT * FROM doanhthu_excel WHERE YEAR(order_date) = {compare_year}"
        if location:
            query_compare += f" AND city = '{location}'"

        try:
            # Truy vấn dữ liệu cho năm hiện tại
            data_current = db.read_query(query_current)
            if data_current.empty:
                result_label.config(text="Không có dữ liệu cho năm hiện tại.")
                return
            processed_data_current = process_data(data_current)
            monthly_sales_current = processed_data_current.groupby('Month')['sales'].sum().reset_index()

            # Truy vấn dữ liệu cho năm so sánh
            data_compare = db.read_query(query_compare)
            if data_compare.empty:
                result_label.config(text="Không có dữ liệu cho năm so sánh.")
                return
            processed_data_compare = process_data(data_compare)
            monthly_sales_compare = processed_data_compare.groupby('Month')['sales'].sum().reset_index()

            # Vẽ biểu đồ so sánh
            visualize_comparison(monthly_sales_current, monthly_sales_compare, None, None, compare_month)

            result_label.config(text=f"So sánh doanh thu giữa {year} và {compare_year}.")
        except Exception as e:
            result_label.config(text=f"Lỗi phân tích: {e}")

    # Trường hợp người dùng chọn tháng để so sánh (so sánh giữa 2 tháng)
    elif month and compare_month:
        # Xây dựng truy vấn SQL cho tháng hiện tại
        query_current = f"SELECT * FROM doanhthu_excel WHERE YEAR(order_date) = {year} AND MONTH(DATE(order_date)) = {month}"
        if location:
            query_current += f" AND city = '{location}'"

        # Xây dựng truy vấn SQL cho tháng so sánh
        query_compare = f"SELECT * FROM doanhthu_excel WHERE YEAR(order_date) = {compare_year} AND MONTH(DATE(order_date)) = {compare_month}"
        if location:
            query_compare += f" AND city = '{location}'"

        try:
            # Truy vấn dữ liệu cho tháng hiện tại
            data_current = db.read_query(query_current)
            if data_current.empty:
                result_label.config(text="Không có dữ liệu cho tháng hiện tại.")
                return
            processed_data_current = process_data(data_current)
            daily_sales_current = processed_data_current.groupby('Day')['sales'].sum().reset_index()

            # Truy vấn dữ liệu cho tháng so sánh
            data_compare = db.read_query(query_compare)
            if data_compare.empty:
                result_label.config(text="Không có dữ liệu cho tháng so sánh.")
                return
            processed_data_compare = process_data(data_compare)
            daily_sales_compare = processed_data_compare.groupby('Day')['sales'].sum().reset_index()

            # Vẽ biểu đồ so sánh
            visualize_comparison(None, None, daily_sales_current, daily_sales_compare, compare_month)

            result_label.config(text=f"So sánh doanh thu giữa tháng {month}/{year} và tháng {compare_month}/{compare_year}.")
        except Exception as e:
            result_label.config(text=f"Lỗi phân tích: {e}")

def visualize_comparison(monthly_sales_current, monthly_sales_compare, daily_sales_current, daily_sales_compare, compare_month):
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # Tạo 2 biểu đồ trong 1 hàng
    
    year = selected_year.get()
    compare_year = selected_year_compare.get()  # Năm so sánh
    month = selected_month.get()
    compare_month = selected_month_compare.get()  # Tháng so sánh
    
    clear_canvas()

    # Trường hợp so sánh giữa 2 năm (biểu đồ đường và cột)
    if not month and not compare_month:
        # Biểu đồ đường: Doanh thu theo tháng cho cả 2 năm
        axes[0].plot(monthly_sales_current['Month'], monthly_sales_current['sales'], label=f"{year}", marker='o', color='blue')
        axes[0].plot(monthly_sales_compare['Month'], monthly_sales_compare['sales'], label=f"{compare_year}", marker='o', color='red')
        axes[0].set_title(f"Doanh thu theo tháng: {year} vs {compare_year}")
        axes[0].set_xlabel("Tháng")
        axes[0].set_ylabel("Doanh thu (VND)")
        axes[0].set_xticks(range(1, 13))
        axes[0].grid(True)
        axes[0].legend()

         # Định dạng trục y và giảm kích thước font để không bị đè lên
        axes[0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        axes[0].tick_params(axis='y', labelsize=6)  # Giảm kích thước font của trục y
        # Biểu đồ cột: Tổng doanh thu cho 2 năm
        axes[1].bar([year, compare_year], [monthly_sales_current['sales'].sum(), monthly_sales_compare['sales'].sum()], color=['blue', 'red'])
        axes[1].set_title(f"Tổng doanh thu: {year} vs {compare_year}")
        axes[1].set_xlabel("Năm")
        axes[1].set_ylabel("Tổng doanh thu (VND)")
        axes[1].grid(True)

         # Định dạng trục y và giảm kích thước font để không bị đè lên
        axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        axes[1].tick_params(axis='y', labelsize=6)  # Giảm kích thước font của trục y
    # Trường hợp so sánh giữa 2 tháng (biểu đồ đường và cột)
    elif month and compare_month:
        # Biểu đồ đường: Doanh thu theo ngày cho tháng hiện tại và tháng so sánh
        axes[0].plot(daily_sales_current['Day'], daily_sales_current['sales'], label=f"Tháng {month}/{year}", marker='o', color='blue')
        axes[0].plot(daily_sales_compare['Day'], daily_sales_compare['sales'], label=f"Tháng {compare_month}/{compare_year}", marker='o', color='red')
        axes[0].set_title(f"Doanh thu theo ngày: {month}/{year} vs {compare_month}/{compare_year}")
        axes[0].set_xlabel("Ngày")
        axes[0].set_ylabel("Doanh thu (VND)")
        axes[0].set_xticks(range(1, 32, 3))  # Hiển thị theo ngày cách 3 ngày
        axes[0].grid(True)
        axes[0].legend()

         # Định dạng trục y và giảm kích thước font để không bị đè lên
        axes[0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        axes[0].tick_params(axis='y', labelsize=6)  # Giảm kích thước font của trục y
        # Biểu đồ cột: Tổng doanh thu cho 2 tháng
        axes[1].bar([month, compare_month], [daily_sales_current['sales'].sum(), daily_sales_compare['sales'].sum()], color=['blue', 'red'])
        axes[1].set_title(f"Tổng doanh thu: Tháng {month}/{year} vs Tháng {compare_month}/{compare_year}")
        axes[1].set_xlabel("Tháng")
        axes[1].set_ylabel("Tổng doanh thu (VND)")
        axes[1].grid(True)
        axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        axes[1].tick_params(axis='y', labelsize=6)  # Giảm kích thước font của trục y
    # Hiển thị biểu đồ trong Tkinter
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def clear_canvas():
    for widget in canvas_frame.winfo_children():
        widget.destroy()

def clear_forecast_canvas():
    for widget in forecast_canvas_frame.winfo_children():
        widget.destroy()
    forecast_canvas_frame.pack_forget()  # 👈 đảm bảo ẩn hoàn toàn

# Cập nhật danh sách thành phố theo năm
def update_locations(event=None):
    year = selected_year.get()
    try:
        df = db.read_query(f"SELECT DISTINCT city FROM doanhthu_excel WHERE YEAR(order_date) = {year}")
        cities = [''] + sorted(df['city'].dropna().unique().tolist())
        selected_location['values'] = cities
        selected_location.set('')
    except:
        selected_location['values'] = ['']

# Giao diện Tkinter
# Giao diện Tkinter
root = tk.Tk()
root.title("Phân tích Doanh thu Bán hàng")

# Tạo một frame để chứa các thanh chọn
frame_select = tk.Frame(root)
frame_select.pack(pady=10)

# Thêm thanh chọn năm vào frame
tk.Label(frame_select, text="Chọn năm:").pack(side="left", padx=10)
selected_year = ttk.Combobox(frame_select, values=['2021', '2022', '2023', '2024', '2025'], state="readonly")
selected_year.set("2021")
selected_year.pack(side="left", padx=10)

# Thêm thanh chọn tháng vào frame
tk.Label(frame_select, text="Chọn tháng:").pack(side="left", padx=10)
selected_month = ttk.Combobox(frame_select, values=[''] + [str(i) for i in range(1, 13)], state="readonly")
selected_month.set('')
selected_month.pack(side="left", padx=10)

# Thêm thanh chọn địa điểm vào frame
tk.Label(frame_select, text="Chọn địa điểm:").pack(side="left", padx=10)
selected_location = ttk.Combobox(frame_select, state="readonly")
selected_location.pack(side="left", padx=10)

# Thêm thanh chọn năm so sánh và tháng so sánh vào frame
tk.Label(frame_select, text="Chọn năm so sánh:").pack(side="left", padx=10)
selected_year_compare = ttk.Combobox(frame_select, values=['2021', '2022', '2023', '2024', '2025'], state="readonly")
selected_year_compare.set("2021")
selected_year_compare.pack(side="left", padx=10)

tk.Label(frame_select, text="Chọn tháng so sánh:").pack(side="left", padx=10)
selected_month_compare = ttk.Combobox(frame_select, values=[''] + [str(i) for i in range(1, 13)], state="readonly")
selected_month_compare.set('')
selected_month_compare.pack(side="left", padx=10)

tk.Button(root, text="So sánh theo năm, tháng và địa điểm", command=compare_by_year_month_location).pack(pady=10)

selected_year.bind("<<ComboboxSelected>>", update_locations)
update_locations()
tk.Button(root, text="dự báo doanh thu", command=run_sales_forecast).pack(pady=10)


tk.Button(root, text="Nhập dữ liệu từ Excel", command=import_and_save_data).pack(pady=10)

tk.Button(root, text="Phân tích", command=run_analysis).pack(pady=10)
result_label = tk.Label(root, text="", wraplength=400, justify="left")
result_label.pack(pady=10)
canvas_frame = tk.Frame(root)
canvas_frame.pack(pady=10)

forecast_canvas_frame = tk.Frame(root)


root.mainloop()
