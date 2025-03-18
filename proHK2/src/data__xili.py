import matplotlib.pyplot as plt

def visualize_data(monthly_sales, hourly_sales):
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_sales['Month'], monthly_sales['sales'], marker='o')
    plt.title('Doanh số theo tháng')
    plt.xlabel('Tháng')
    plt.ylabel('Doanh số')
    plt.xticks(monthly_sales['Month'])
    plt.grid()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.bar(hourly_sales['Hour'], hourly_sales['sales'])
    plt.title('Doanh số theo giờ')
    plt.xlabel('Giờ trong ngày')
    plt.ylabel('Doanh số')
    plt.xticks(hourly_sales['Hour'])
    plt.grid()
    plt.show()