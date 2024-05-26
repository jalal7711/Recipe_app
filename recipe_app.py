from tabulate import tabulate
from mysql.connector import Error

class RecipeManager:
    def __init__(self, db):
        self.db = db

    def list_categories(self):
        cursor = self.db.get_cursor()
        if cursor:
            cursor.execute("SELECT id, name FROM categories order by id")
            categories = cursor.fetchall()
            print("Available categories:")
            for category in categories:
                print(f"ID: {category['id']}, Name: {category['name']}")
            cursor.close()

    def add_recipe(self, user_id):
        cursor = self.db.get_cursor()
        if cursor:
            self.list_categories()
            title = input("Enter recipe title: ")
            instructions = input("Enter instructions: ")
            category_id = int(input("Enter category ID: "))
            try:
                cursor.execute(
                    "INSERT INTO recipes (title, instructions, category_id, user_id) VALUES (%s, %s, %s, %s)",
                    (title, instructions, category_id, user_id)
                )
                recipe_id = cursor.lastrowid

                while True:
                    ingredient_name = input("Enter ingredient name (or 'done' to finish): ")
                    if ingredient_name.lower() == 'done':
                        break
                    amount = input(f"Enter amount for {ingredient_name}: ")
                    cursor.execute("SELECT id FROM ingredients WHERE name=%s", (ingredient_name,))
                    ingredient = cursor.fetchone()
                    if ingredient:
                        ingredient_id = ingredient['id']
                    else:
                        cursor.execute("INSERT INTO ingredients (name) VALUES (%s)", (ingredient_name,))
                        ingredient_id = cursor.lastrowid
                    cursor.execute(
                        "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount) VALUES (%s, %s, %s)",
                        (recipe_id, ingredient_id, amount)
                    )
                print("Recipe added successfully!")
            except Error as err:
                print(f"Error: {err}")
            finally:
                cursor.close()

    def view_recipes(self):
        cursor = self.db.get_cursor()
        if cursor:
            cursor.execute(
                "SELECT r.id, r.title, c.name AS category, u.username AS author "
                "FROM recipes r "
                "JOIN categories c ON r.category_id = c.id "
                "JOIN users u ON r.user_id = u.id"
            )
            recipes = cursor.fetchall()

            table_data = []

            for recipe in recipes:
                cursor.execute(
                    "SELECT i.name, ri.amount "
                    "FROM recipe_ingredients ri "
                    "JOIN ingredients i ON ri.ingredient_id = i.id "
                    "WHERE ri.recipe_id=%s", (recipe['id'],)
                )
                ingredients = cursor.fetchall()
                ingredients_list = [f"{ingredient['name']}: {ingredient['amount']}" for ingredient in ingredients]
                table_data.append([recipe['id'], recipe['title'], recipe['category'], recipe['author'], "\n".join(ingredients_list)])

            headers = ["ID", "Title", "Category", "Author", "Ingredients"]
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
            cursor.close()
            
    def show_recipe_instructions(self, recipe_name):
        cursor = self.db.get_cursor()
        if cursor:
            try:
                # Fetch the recipe based on case-insensitive search
                cursor.execute("SELECT id, instructions FROM recipes WHERE LOWER(title) = LOWER(%s)", (recipe_name,))
                recipe = cursor.fetchone()
                if recipe:
                    print("Recipe Instructions:") 
                    print()
                    print(recipe['instructions'])
                else:
                    print("Recipe not found!")
            except Error as err:
                print(f"Error: {err}")
            finally:
                print()
                cursor.close()

    def delete_recipe(self, recipe_id):
        cursor = self.db.get_cursor()
        if cursor:
            try:
                # First, delete associated ingredients
                cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s", (recipe_id,))
                
                # Then, delete the recipe itself
                cursor.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
                
                print("Recipe deleted successfully!")
                self.db.connection.commit()
            except Error as err:
                print(f"Error: {err}")
            finally:
                cursor.close()

    def add_category(self):
        cursor = self.db.get_cursor()
        if cursor:
            category_name = input("Enter category name: ")
            try:
                cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
                print("Category added successfully!")
            except Error as err:
                print(f"Error: {err}")
            finally:
                cursor.close()

class RecipeFilter:
    def __init__(self, db):
        self.db = db

    def filter_recipes_by_category(self):
        cursor = self.db.get_cursor()
        if cursor:
            cursor.execute("SELECT id, name FROM categories")
            categories = cursor.fetchall()
            print("Available categories:")
            for category in categories:
                print(f"ID: {category['id']}, Name: {category['name']}")
            
            category_name = input("Enter the category Name to filter by: ")  # Update prompt here
            cursor.execute(
                "SELECT r.id, r.title, c.name AS category, u.username AS author "
                "FROM recipes r "
                "JOIN categories c ON r.category_id = c.id "
                "JOIN users u ON r.user_id = u.id "
                "WHERE c.name = %s", (category_name,)
            )
            recipes = cursor.fetchall()

            table_data = []

            for recipe in recipes:
                cursor.execute(
                    "SELECT i.name, ri.amount "
                    "FROM recipe_ingredients ri "
                    "JOIN ingredients i ON ri.ingredient_id = i.id "
                    "WHERE ri.recipe_id=%s", (recipe['id'],)
                )
                ingredients = cursor.fetchall()
                ingredients_list = [f"{ingredient['name']}: {ingredient['amount']}" for ingredient in ingredients]
                table_data.append([recipe['id'], recipe['title'], recipe['category'], recipe['author'], "\n".join(ingredients_list)])

            headers = ["ID", "Title", "Category", "Author", "Ingredients"]
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
            cursor.close()
