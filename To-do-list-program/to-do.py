import sqlite3
from datetime import datetime
database = 'akshay.db'  # <--- CHANGED HERE
LOGGED_IN_USER_ID=None
def connect():
    conn=sqlite3.connect(database)
    return conn
def setup():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL -- Storing password in plain text for simplicity per request
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL, -- High, Medium, Low
            due_date TEXT NOT NULL, -- YYYY-MM-DD
            created_date TEXT NOT NULL, 
            is_complete INTEGER DEFAULT 0, -- 0 (False) or 1 (True)
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''') 
    conn.commit()
    conn.close()
    print("Database setup complete.")
def register(username, password):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, password))
        conn.commit()
        print(f"\nUser '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print("\nError: Username already exists.")
    finally:
        conn.close()
def login(username, password):
    global LOGGED_IN_USER_ID
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", 
                   (username, password))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        LOGGED_IN_USER_ID = user_data[0] 
        print(f"\nLogin successful. Welcome, {username}!")
        return True
    else:
        print("\nInvalid username or password.")
        return False
def add_task(description, priority, due_date):
    if not LOGGED_IN_USER_ID:
        print("Please login first.")
        return
    conn = connect()
    cursor = conn.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')
    try:
        cursor.execute(
            """INSERT INTO tasks (user_id, description, priority, due_date, created_date) 
               VALUES (?, ?, ?, ?, ?)""", 
            (LOGGED_IN_USER_ID, description, priority, due_date, current_date)
        )
        conn.commit()
        print("\nTask added successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
def view_tasks(show=False):
    if not LOGGED_IN_USER_ID:
        print("Please login first.")
        return
    conn = connect()
    cursor = conn.cursor()
    complete= "AND is_complete = 0" if not show else ""
    cursor.execute(
        f"""SELECT task_id, description, priority, due_date, is_complete
            FROM tasks 
            WHERE user_id = ? {complete}
            ORDER BY 
                CASE priority 
                    WHEN 'High' THEN 1 
                    WHEN 'Medium' THEN 2 
                    WHEN 'Low' THEN 3 
                    ELSE 4 
                END, 
                due_date ASC""", 
        (LOGGED_IN_USER_ID,)
    )
    tasks = cursor.fetchall()
    conn.close()
    if not tasks:
        print("\nYour to-do list is empty.")
        return
    status = "Status" if show else " "
    print("\n--- YOUR TO-DO LIST ---")
    print(f"{'ID':<4} | {'Priority':<8} | {'Due Date':<10} | {status:<8} | {'Task Description'}")
    print("-" * 65)
    for task in tasks:
        task_id, desc, prio, due, completed = task
        status = "DONE" if completed == 1 else "ACTIVE"
        print(f"{task_id:<4} | {prio:<8} | {due:<10} | {status:<8} | {desc}")
    print("-" * 65)
def update_task_status(task_id, complete=True):
    if not LOGGED_IN_USER_ID:
        print("Please login first.")
        return
    conn = connect()
    cursor = conn.cursor()
    new_status = 1 if complete else 0
    cursor.execute(
        """UPDATE tasks SET is_complete = ? WHERE task_id = ? AND user_id = ?""",
        (new_status, task_id, LOGGED_IN_USER_ID)
    )
    conn.commit()
    if cursor.rowcount > 0:
        action = "COMPLETED" if complete else "set back to ACTIVE"
        print(f"\nTask ID {task_id} successfully marked as {action}.")
    else:
        print(f"\nError: Task ID {task_id} not found or does not belong to you.")
    conn.close()
def delete_task(task_id):
    if not LOGGED_IN_USER_ID:
        print("Please login first.")
        return
        
    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute(
        """DELETE FROM tasks WHERE task_id = ? AND user_id = ?""",
        (task_id, LOGGED_IN_USER_ID)
    )
    conn.commit()
    if cursor.rowcount > 0:
        print(f"\nTask ID {task_id} permanently deleted.")
    else:
        print(f"\nError: Task ID {task_id} not found or does not belong to you.")
    conn.close()
def delete_all_tasks():
    if not LOGGED_IN_USER_ID:
        print("Please login first.")
        return
    confirm = input("ARE YOU SURE you want to delete ALL your tasks? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Deletion cancelled.")
        return
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE user_id = ?", (LOGGED_IN_USER_ID,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"\nSuccessfully deleted {cursor.rowcount} task(s). Your list is now empty.")
    else:
        print("\nYou had no tasks to delete.")
    conn.close()
def main_menu():
    global LOGGED_IN_USER_ID
    while True:
        if not LOGGED_IN_USER_ID:
            print("\n--- WELCOME ---")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
                u = input("Username: ")
                p = input("Password (simple text): ")
                register(u, p)
            elif choice == '2':
                u = input("Username: ")
                p = input("Password: ")
                login(u, p)
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        else:
            print("\n--- TASK MANAGER ---")
            print("1. View Active Tasks")
            print("2. Add New Task")
            print("3. Mark Task Complete")
            print("4. Delete Specific Task")
            print("5. Delete ALL My Tasks")
            print("6. Logout")
            choice = input("Enter choice: ")
            if choice == '1':
                view_tasks()
            elif choice == '2':
                desc = input("Task Description: ")
                prio = input("Priority (High/Medium/Low): ").capitalize()
                if prio not in ['High', 'Medium', 'Low']:
                    print("Invalid priority. Task not added.")
                    continue
                due = input("Due Date (YYYY-MM-DD): ")
                add_task(desc, prio, due)
            elif choice == '3':
                view_tasks()
                try:
                    task_id = int(input("Enter Task ID to Mark COMPLETE: "))
                    update_task_status(task_id, complete=True)
                except ValueError:
                    print("Invalid ID.")
            elif choice == '4':
                view_tasks()
                try:
                    task_id = int(input("Enter Task ID to DELETE permanently: "))
                    delete_task(task_id)
                except ValueError:
                    print("Invalid ID.")
            elif choice == '5':
                delete_all_tasks()
            elif choice == '6':
                LOGGED_IN_USER_ID = None
                print("Logged out successfully.")
            else:
                print("Invalid choice.")
setup()
main_menu()
