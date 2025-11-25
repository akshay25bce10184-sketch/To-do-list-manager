TASK-MANAGER-

Secure CLI Task Manager

A robust, command-line based Task Manager application built with Python. It features a persistent SQLite database to store tasks and implements SHA-256 hashing to securely store user passwords.

🚀 Features

User Authentication:

Secure Registration & Login.

Security: Passwords are hashed using SHA-256 before storage. Plain text passwords are never saved in the database.

Task Management:

Add Tasks: Set descriptions, priorities (High/Medium/Low), and due dates.

View Tasks: automatically sorted by Priority first, then Due Date.

Update Status: Mark tasks as Complete or Active.

Delete: Remove specific tasks or wipe all tasks for the logged-in user.

Data Persistence: All data is saved to sarthak.db using SQLite3.

Relational Data: Tasks are strictly linked to specific User IDs (users cannot see each other's tasks).

📋 Prerequisites

Python 3.x installed on your machine.

No external libraries are required! This project uses only Python's standard libraries:

sqlite3

datetime

hashlib

🛠️ Installation & Setup

Download the code: Save the python script as task_manager.py.

Run the application: Open your terminal or command prompt, navigate to the folder, and run:

python task_manager.py

First Run: The application will automatically create a file named sarthak.db in the same directory.

🎮 How to Use

Main Menu
When you start the app, you will see:

--- WELCOME ---

Register
Login
Exit
Register: Create a new account. (e.g., Username: admin, Password: password123)

Login: Enter your credentials to access your tasks.

Task Menu (After Login)
--- TASK MANAGER ---

View Active Tasks
Add New Task
Mark Task Complete
Delete Specific Task
Delete ALL My Tasks
Logout
Adding a Task:

Enter description.

Enter Priority (High, Medium, or Low).

Enter Date in YYYY-MM-DD format (e.g., 2023-12-25).

Viewing Tasks:

Tasks are displayed in a formatted table.

High priority tasks always appear at the top.

🔒 Security Explanation

This application uses SHA-256 Hashing for password storage.

When a user registers, the password mypassword is converted into a hash: 5e88489....

This hash is stored in the database.

When logging in, the input is hashed again and compared to the stored version.

Benefit: If the database file (sarthak.db) is stolen or viewed, the attacker cannot see the actual user passwords.

📂 Project Structure

. ├── task_manager.py # Main application code ├── sarthak.db # Database file (created auto-magically) └── README.md # This documentation

⚠️ Troubleshooting

"Database is locked": Make sure you don't have the database open in a DB Browser program while trying to write to it via Python.

"Invalid Password": If you upgraded from a previous version without hashing, delete the old sarthak.db file and register again.
