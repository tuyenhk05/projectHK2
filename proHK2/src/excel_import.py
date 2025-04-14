import pandas as pd

def import_excel(file_path):
    try:
        data = pd.read_excel(file_path)

        # Chu?n h�a d? li?u
        data['order_date'] = pd.to_datetime(data['order_date'], errors='coerce')
        data.dropna(subset=['order_date'], inplace=True)  # Lo?i b? d? li?u l?i ng�y th�ng

        # Ki?m tra c�c c?t c?n thi?t
        required_columns = ['order_date', 'city', 'product_id', 'quantity', 'sales']
        if not all(col in data.columns for col in required_columns):
            raise ValueError("Loi")

        return data
    except Exception as e:
        print(f"Loi khi doc file Excel: {e}")
        return pd.DataFrame()
