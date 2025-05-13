# To-Do-or-Not-To-Do
A Python-based desktop To-Do List application with a graphical user interface built using Tkinter. The app connects to a MySQL database to manage and persist tasks with features like priority levels, deadlines, status tracking, and starring important items.

# Features
Add, delete, and complete tasks

Set priority levels (Low, Medium, High)

Set deadlines (with input validation)

Star/unstar important tasks

Filter tasks by priority

Toggle views for starred and completed tasks

GUI built with Tkinter

Task data stored in MySQL for persistence

# Requirements
Python 3.x

MySQL Server

Python packages:

mysql-connector-python

tkinter (usually included with Python)

# MySQL Setup
Before running the application, ensure that:

MySQL server is running.

A database named todolistapp exists.

The following table is created automatically when the app is run for the first time.


You can modify the database configuration in the script:

```
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'todolistapp'
}
```
# How to Use
Run the Python script.

Use the input fields to add a new task with a priority and deadline (YYYY/MM/DD format).

Select a task from the list to:

Delete it

Mark it as completed

Star/unstar it

Use the buttons and slider to filter tasks by status or priority.

# Notes
Ensure that image files like iconphoto.png and random.png are present in the same directory as the script.

The UI is responsive and styled with a consistent color scheme for an enhanced user experience.











