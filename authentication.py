from getpass import getpass
from mysql.connector import Error

class AuthenticationManager:
    def __init__(self, db):
        self.db = db

    def register_user(self):
        cursor = self.db.get_cursor()
        if cursor:
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                print("User registered successfully!")
            except Error as err:
                print(f"Error: {err}")
            finally:
                cursor.close()

    def login_user(self):
        cursor = self.db.get_cursor()
        if cursor:
            username = input("Enter username: ")
            password = getpass("Enter password: ")
            cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            if user:
                print("Login successful!")
                return user['id']  # Return user_id
            else:
                print("Invalid credentials!")
                return None
        return None
