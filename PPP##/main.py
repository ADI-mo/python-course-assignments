from planner import MealPlanner
from edamam_service import EdamamService
from cost_calculator import estimate_budget

def run_app():
    # 1. קונפיגורציה
    config = {'kosher': True, 'diet': 'Standard', 'max_time': 45, 'participants': 4}
    
    # 2. טעינת נתונים
    planner = MealPlanner('data/recipes.json', 'data/pantry.json')
    api = EdamamService()
    
    print("Fetching extra recipes from API...")
    online_data = api.fetch_recipes("healthy", diet=config['diet'], max_time=config['max_time'])
    
    # 3. יצירת תפריט
    menu = planner.generate_plan(config, online_data)
    
    # 4. רשימת קניות ועלויות
    shop_list = planner.get_shopping_list()
    budget = estimate_budget(shop_list, 'data/cbs_prices.csv')

    # 5. הדפסת תוצאות
    print(f"\nWeekly Plan Generated! Estimated Cost: {budget} ILS")
    for day, meals in menu.items():
        print(f"{day}: {meals.get('Lunch', {}).get('name')} & {meals.get('Dinner', {}).get('name')}")

if __name__ == "__main__":
    run_app()