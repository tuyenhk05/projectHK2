def analyze_data(data):
    monthly_sales = data.groupby(['Year', 'Month'])['sales'].sum().reset_index()
    best_month = monthly_sales.loc[monthly_sales['sales'].idxmax()]

    city_sales = data.groupby('city')['sales'].sum().reset_index()
    best_city = city_sales.loc[city_sales['sales'].idxmax()]

    hourly_sales = data.groupby('Hour')['sales'].sum().reset_index()

    top_products = data.groupby('product_id')['quantity'].sum().reset_index()
    best_selling_product = top_products.loc[top_products['quantity'].idxmax()]

    return best_month, best_city, hourly_sales, best_selling_product