import sqlite3
import bcrypt

# connect to database or create it if it doesn't exist
conn = sqlite3.connect('tdg_user.db')
cursor = conn.cursor()

# create table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT UNIQUE,
#         password TEXT,
#         progress TEXT
#     )
# ''')

# conn.commit()

# function to add a user to the database
def add_user(username, password, progress):
    # Connect to the database
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()
        
    # Passwort hashen
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute("INSERT INTO users (username, password, progress) VALUES (?, ?, ?)", 
                       (username, hashed_pw, progress))
        conn.commit()
        print("Added user successfully.")
        return True
    except sqlite3.IntegrityError:
        print("User already exists.")
        return False

# update a user's progress
def update_user_progress(username, new_progress):
    # Connect to the database
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    if result:
        # Aktualisiere den Spielfortschritt
        cursor.execute("UPDATE users SET progress = ? WHERE username = ?", 
                       (new_progress, username))
        conn.commit()
        print("Progress successfully updated.")
    else:
        print("User not found.")


# add a user to the database
# add_user("player2", "Binchilling", '{"level": 20, "points": 5500}')

# function to get a user's progress if the user exists
def get_user_progress(username :str) -> str:
    # Connect to the database
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()

    cursor.execute("SELECT progress FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        return result[0]  # return the progress
    else:
        return "User not found."
    
def verify_user(username :str, password :str) -> str:
    # Connect to the database
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()

    """Verify the user's password."""
    # get the hashed password from the database
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        hashed_pw = result[0]  # the hashed password as a string
        # check if the password is correct
        if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
            return "Login successful."
        else:
            return "Wrong password."
    else:
        return "User not found."


# example usage of get_user_progress
# print(get_user_progress("player2"))
# update_user_progress("player2", '{"level": 25, "points": 6000}')
print(verify_user("player2", "Binchilling"))
# close the connection
conn.close()
