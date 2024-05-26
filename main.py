from database import Database
from authentication import AuthenticationManager
from recipe_app import RecipeManager, RecipeFilter

def main():
    db = Database(host='localhost', user='root', password='83@9%1&703*3jal', database='recipe_app')
    db.connect()

    if not db.connection or not db.connection.is_connected():
        print("Unable to connect to the database. Please check your credentials and database server.")
        return

    auth_manager = AuthenticationManager(db)
    recipe_manager = RecipeManager(db)
    recipe_filter = RecipeFilter(db)

    user_id = None  # Initialize user_id to None

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Add Recipe")
        print("4. View Recipes")
        print("5. Show Recipe Instructions")
        print("6. Delete Recipe")
        print("7. Add Category")
        print("8. Filter Recipes by Category")
        print("9. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            auth_manager.register_user()

        elif choice == '2':
            user_id = auth_manager.login_user()

        elif choice == '3':
            if user_id:
                recipe_manager.add_recipe(user_id)
            else:
                print("Please login first.")

        elif choice == '4':
            recipe_manager.view_recipes()   

        elif choice == '5':
            recipe_name = input("Enter the name of the recipe to view instructions: ")
            print()
            recipe_manager.show_recipe_instructions(recipe_name)

        elif choice == '6':
            if user_id:
                recipe_id = input("Enter recipe ID to delete: ")
                recipe_manager.delete_recipe(recipe_id)
            else:
                print("Please login first.")

        elif choice == '7':
            if user_id:
                recipe_manager.add_category()
            else:
                print("Please login first.")

        elif choice == '8':
            recipe_filter.filter_recipes_by_category()

        elif choice == '9':
            break
        else:
            print("Invalid choice.")

        db.connection.commit()

    db.close()

if __name__ == '__main__':
    main()
