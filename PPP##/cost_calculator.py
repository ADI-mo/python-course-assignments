import pandas as pd

def estimate_budget(shopping_list, cbs_data_path):
    try:
        prices_df = pd.read_csv(cbs_data_path)
        total = 0
        for item, qty in shopping_list.items():
            # חיפוש מחיר לפי מילת מפתח
            match = prices_df[prices_df['item'].str.contains(item, case=False, na=False)]
            price = match['avg_price'].values[0] if not match.empty else 10 # ברירת מחדל
            total += price * qty
        return round(total, 2)
    except Exception: return 0.0