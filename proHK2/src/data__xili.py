import matplotlib.pyplot as plt

def visualize_data(monthly_sales, hourly_sales):
    plt.figure(figsize=(12, 6))

    # Biểu đồ 1 - Doanh số theo tháng
    plt.subplot(1, 2, 1)  # (1 hàng, 2 cột, vị trí 1)
    plt.plot(monthly_sales['Month'], monthly_sales['sales'], marker='o')
    plt.title('Doanh số theo tháng')
    plt.xlabel('Tháng')
    plt.ylabel('Doanh số')
    plt.xticks(monthly_sales['Month'])
    plt.grid()

    # Biểu đồ 2 - Doanh số theo giờ
    plt.subplot(1, 2, 2)  # (1 hàng, 2 cột, vị trí 2)
    plt.bar(hourly_sales['Hour'], hourly_sales['sales'])
    plt.title('Doanh số theo giờ')
    plt.xlabel('Giờ trong ngày')
    plt.ylabel('Doanh số')
    plt.xticks(hourly_sales['Hour'])
    plt.grid()

    plt.tight_layout()  # Đảm bảo các biểu đồ không bị chồng lên nhau
    plt.show()
