import pandas as pd

def get_estimated_cost(shopping_list):
    # כאן ניתן לטעון קובץ CSV שהורד מה-CBS
    prices_df = pd.read_csv('data/cbs_prices.csv') 
    total_cost = 0
    for item, qty in shopping_list.items():
        # חיפוש מחיר ממוצע ליחידה
        avg_price = prices_df[prices_df['item'] == item]['avg_price'].values[0]
        total_cost += avg_price * qty
    return total_cost