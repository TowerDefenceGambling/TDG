import sqlite3
import bcrypt

# Function to add a user to the database
def add_user(username, password, progress):
    """
    Adds a new user to the database with hashed password and initial progress.
    Returns True if the user is added successfully, and False if the username already exists.
    """
    # Connect to the database
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()

        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Insert new user into the users table
            cursor.execute("INSERT INTO users (username, password, progress) VALUES (?, ?, ?)", 
                           (username, hashed_pw, progress))
            conn.commit()
            print("Added user successfully.")
            return True
        except sqlite3.IntegrityError:
            print("User already exists.")
            return False

# Function to update a user's progress
def update_user_progress(username, new_progress):
    """
    Updates the progress of an existing user.
    """
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            # Update the user's progress
            cursor.execute("UPDATE users SET progress = ? WHERE username = ?", 
                           (new_progress, username))
            conn.commit()
            print("Progress successfully updated.")
        else:
            print("User not found.")

# Function to get a user's progress if the user exists
def get_user_progress(username: str) -> str:
    """
    Retrieves the progress of a user from the database.
    """
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT progress FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the progress
        else:
            return "User not found."

# Function to verify the user's credentials
def verify_user(username: str, password: str) -> str:
    """
    Verifies the user's password by comparing the stored hashed password with the provided password.
    """
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()

        # Get the hashed password from the database
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            hashed_pw = result[0]  # Stored hashed password
            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
                return "Login successful."
            else:
                return "Wrong password."
        else:
            return "User not found."

# Example usage of get_user_progress
# print(get_user_progress("player2"))
# update_user_progress("player2", '{"level": 25, "points": 6000}')
# print(verify_user("player2", "Binchilling"))
