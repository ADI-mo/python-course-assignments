import json
import random

class MealPlanner:
    def __init__(self, recipes_path, pantry_path):
        self.local_recipes = self._load_json(recipes_path)
        self.pantry = self._load_json(pantry_path)
        self.weekly_menu = {}

    def _load_json(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError: return {} if "pantry" in path else []

    def check_kosher(self, day_meals, new_meal, is_kosher_enabled):
        if not is_kosher_enabled or new_meal['type'] == 'Parve': return True
        for m in day_meals.values():
            if {m['type'], new_meal['type']} == {'Meat', 'Dairy'}: return False
        return True

    def generate_plan(self, config, online_recipes=[]):
        all_recipes = self.local_recipes + online_recipes
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        
        for day in days:
            self.weekly_menu[day] = {}
            for meal_time in ['Lunch', 'Dinner']:
                # סינון לפי העדפות זמן ודיאטה
                candidates = [r for r in all_recipes if r['prep_time'] <= config['max_time']]
                if config['diet'] == 'Vegan': candidates = [r for r in candidates if r['is_vegan']]
                elif config['diet'] == 'Vegetarian': candidates = [r for r in candidates if r['is_vegetarian']]

                random.shuffle(candidates)
                for res in candidates:
                    if self.check_kosher(self.weekly_menu[day], res, config['kosher']):
                        self.weekly_menu[day][meal_time] = res
                        break
        return self.weekly_menu

    def get_shopping_list(self):
        needed = {}
        for day in self.weekly_menu.values():
            for meal in day.values():
                for ing, qty in meal['ingredients'].items():
                    # אופטימיזציה מול המזווה
                    pantry_qty = self.pantry.get(ing, 0)
                    final_qty = max(0, qty - pantry_qty)
                    if final_qty > 0:
                        needed[ing] = needed.get(ing, 0) + final_qty
        return needed