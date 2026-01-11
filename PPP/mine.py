import json
import random

class MealPlanner:
    def __init__(self, recipes_path, pantry_path):
        self.recipes = self._load_json(recipes_path)
        self.pantry = self._load_json(pantry_path)
        self.weekly_menu = {}

    def _load_json(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def filter_recipes(self, preferences):
        """
        סינון מתכונים לפי כשרות, טבעונות וזמן הכנה.
        """
        filtered = []
        for r in self.recipes:
            # בדיקת העדפה תזונתית
            if preferences['diet'] == 'Vegan' and not r.get('is_vegan'):
                continue
            if preferences['diet'] == 'Vegetarian' and not r.get('is_vegetarian'):
                continue
            
            # בדיקת זמן הכנה
            if r['prep_time'] > preferences['max_time']:
                continue
                
            filtered.append(r)
        return filtered

    def check_kosher_integrity(self, day_meals, new_meal, config):
        """
        מוודא הפרדה בין בשר לחלב בהתאם להגדרות.
        """
        if not config['kosher']:
            return True
        
        # אם המנה החדשה פרווה - תמיד תקין
        if new_meal['type'] == 'Parve':
            return True
            
        for meal in day_meals.values():
            if meal['type'] == 'Meat' and new_meal['type'] == 'Dairy':
                return False
            if meal['type'] == 'Dairy' and new_meal['type'] == 'Meat':
                return False
        return True

    def generate_plan(self, config):
        available_recipes = self.filter_recipes(config)
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        
        for day in days:
            self.weekly_menu[day] = {}
            # בחירת ארוחת צהריים וערב
            for meal_time in ['Lunch', 'Dinner']:
                valid_choice = False
                attempts = 0
                while not valid_choice and attempts < 20:
                    candidate = random.choice(available_recipes)
                    if self.check_kosher_integrity(self.weekly_menu[day], candidate, config):
                        self.weekly_menu[day][meal_time] = candidate
                        valid_choice = True
                    attempts += 1
        return self.weekly_menu

    def generate_shopping_list(self):
        shopping_list = {}
        for day, meals in self.weekly_menu.items():
            for time, details in meals.items():
                for ingredient, qty in details['ingredients'].items():
                    # חישוב חוסרים מול המזווה
                    pantry_qty = self.pantry.get(ingredient, 0)
                    needed = max(0, qty - pantry_qty)
                    
                    if needed > 0:
                        shopping_list[ingredient] = shopping_list.get(ingredient, 0) + needed
        return shopping_list

# --- דוגמה להרצה ---
if __name__ == "__main__":
    # הגדרות משתמש לדוגמה
    user_config = {
        'kosher': True,
        'diet': 'Standard', # Standard, Vegetarian, Vegan
        'max_time': 45,     # דקות
        'participants': 4
    }

    # אתחול המערכת (בהנחה שיש קבצי נתונים)
    planner = MealPlanner('data/recipes.json', 'data/pantry.json')
    
    # יצירת תפריט
    menu = planner.generate_plan(user_config)
    
    print("--- תפריט שבועי מומלץ ---")
    for day, meals in menu.items():
        lunch = meals.get('Lunch', {}).get('name', 'N/A')
        dinner = meals.get('Dinner', {}).get('name', 'N/A')
        print(f"{day}: צהריים - {lunch} | ערב - {dinner}")

    # יצירת רשימת קניות
    shop_list = planner.generate_shopping_list()
    print("\n--- רשימת קניות (אחרי בדיקת מזווה) ---")
    for item, qty in shop_list.items():
        print(f"- {item}: {qty}")