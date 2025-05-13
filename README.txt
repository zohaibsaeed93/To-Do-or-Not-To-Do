To-Do or Not To-Do (todolist python application)

Setup Requirements
- Python 3.8 or above
- install the Mysql workbench
- setup your mysql credentials

Installation of required modules
run the requirements.txt file in the terminal using this command:

pip install -r requirements.txt

Or Install required dependencies:

   pip install mysql-connector-python




3. Update `DB_CONFIG` in 'main.py 'with your mysql credentials:
   - DB_HOST = "localhost"
   - DB_USER = "your username"
   - DB_PASSWORD = "your password"
   - DB_NAME = "database name" (either create a table or just use the sys or world database)

Running the Application
Run the main script:

python main.py


This will start the To-Do List application with a Tkinter GUI.


- Add tasks with a priority and deadline.
- Mark tasks as completed.
- Delete tasks from the list.
- Star and unstar tasks.
- Show starred tasks.
- Show completed tasks.
- filter tasks using the priority slider.



