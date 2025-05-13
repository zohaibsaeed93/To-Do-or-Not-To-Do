from tkinter import *
from tkinter import messagebox
from tkinter import font as tkfont
from datetime import datetime
import mysql.connector


DB_CONFIG = {
    'host': 'localhost',
    'user': 'user',
    'password': 'password',
    'database': 'todolistapp'
}

#sql setup
def create_connection():
    try:
        connector = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        return connector
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"unable to connect to the MySQL database: {e}")
        return None
# table setupp

def create_tasks_table():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL,
        priority VARCHAR(50) NOT NULL,
        deadline Varchar(50) NOT NULL,
        status VARCHAR(50) NOT NULL DEFAULT 'Pending',
        starred BOOLEAN NOT NULL DEFAULT 0
    );
    '''
    connector = create_connection()
    if connector:
        try:
            cursor = connector.cursor()

            cursor.execute(create_table_query)
            connector.commit()
            print("Table 'tasks' is created or already exists.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"unable to connect to the table: {e}")
        finally:
            cursor.close()
            connector.close()


create_tasks_table()


def add():
    task = taskEntryBox.get()
    priority = priorityentrybox.get().strip().capitalize()
    deadline = deadlineentrybox.get()
    try:
        if deadline:
            datetime.strptime(deadline, "%Y/%m/%d")
    except ValueError:
        messagebox.showerror("Invalid Date Format", "Please enter the deadline in YYYY/MM/DD format.")
        return

    if priority not in ["High", "Medium", "Low"]:
        messagebox.showerror("Invalid Priority", "Priority must be 'High', 'Medium', or 'Low'. Retry.")
        return

    if task == "" or priority == "" or deadline == "":
        messagebox.showerror("Invalid Data Entry", "The entry boxes have been left empty. Try again.")
        return

    connector = create_connection()
    if connector:
        try:
            cursor = connector.cursor()
            cursor.execute('''INSERT INTO tasks (task, priority, deadline, status, starred)
                               VALUES (%s, %s, %s, %s, %s)''', (task, priority, deadline, "Pending", 0))
            connector.commit()
            tasksLoading()
            cleanBox()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connector.close()



def delete():
    highlighted = listboxtasks.curselection()
    if highlighted:
        taskid = listboxtasks.get(highlighted).split()[0]
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute('DELETE FROM tasks WHERE id=%s', (taskid,))
                connection.commit()
                tasksLoading()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                cursor.close()
                connection.close()
    else:
        messagebox.showerror("Invalid Selection", "No task selected for deletion. Please select a task and try again.")


def complete():
    highlighted = listboxtasks.curselection()
    if highlighted:
        taskid = listboxtasks.get(highlighted).split()[0]
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute('UPDATE tasks SET status=%s WHERE id=%s', ("Completed", taskid))
                connection.commit()
                tasksLoading()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                cursor.close()
                connection.close()
    else:
        messagebox.showerror("Invalid Selection",
                             "No task selected for marking as done. Please select a task and try again.")


def star():
    highlighted = listboxtasks.curselection()
    if highlighted:
        taskid = listboxtasks.get(highlighted).split()[0]
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute('SELECT starred FROM tasks WHERE id=%s', (taskid,))
            currentStar = cursor.fetchone()[0]
            nextStar = 1 if currentStar == 0 else 0
            cursor.execute('UPDATE tasks SET starred=%s WHERE id=%s', (nextStar, taskid))
            connection.commit()
            tasksLoading()
            cursor.close()
            connection.close()
    else:
        messagebox.showerror("Invalid Selection", "Unable to detect a selected task for starring")


def filter_by_priority(priorityNumber):
    priorityTerm = {
        "0": None,
        "1": "Low",
        "2": "Medium",
        "3": "High"
    }

    selectedpriority = priorityTerm[priorityNumber]

    listboxtasks.delete(0, END)
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            if selectedpriority:

                cursor.execute('SELECT * FROM tasks WHERE priority=%s', (selectedpriority,))
            else:

                cursor.execute('SELECT * FROM tasks')

            rows = cursor.fetchall()
            for row in rows:
                listboxtasks.insert(END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | Starred: {row[5]}")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()


def showstarred():
    global show_starred
    show_starred = not show_starred
    tasksLoading(show_starred)


def tasksLoading(show_starred=False):
    listboxtasks.delete(0, END)
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            if show_completed:
                cursor.execute('SELECT * FROM tasks WHERE status="Completed"')
            elif show_starred:
                cursor.execute('SELECT * FROM tasks WHERE starred=1')
            else:
                cursor.execute('SELECT * FROM tasks')
            rows = cursor.fetchall()
            for row in rows:
                listboxtasks.insert(END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | Starred: {row[5]}")
        finally:
            cursor.close()
            connection.close()


def cleanBox():
    taskEntryBox.delete(0, END)
    priorityentrybox.delete(0, END)
    deadlineentrybox.delete(0, END)


def showcompleted():
    global show_completed
    show_completed = not show_completed
    tasksLoading()


window = Tk()
window.title("To-Do or Not To-Do :)")
window.geometry("1000x600")
window.configure(bg="#2f3e45")

icon = PhotoImage(file="iconphoto.png")
window.iconphoto(False, icon)

# main frame that im using for widgets
# label for the title
label1 = Label(window,
               text="To-Do or Not To-Do :)",
               font=("Roboto", 25, "bold"),
               bg="#2f3e45",
               fg="#f5f5f5"
               )
label1.pack(pady=12)
# frame for the widgets

frame1 = Frame(window,
               bg="#2f3e45")
frame1.pack(fill="both", expand=True)



# frame for the buttons
frame2 = Frame(frame1,
               bg="#2f3e45",
               width=150)
frame2.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
frame2.grid_rowconfigure(3, weight=1)
frame2.grid_rowconfigure(6, weight=1)


addButton = Button(frame2,
                   text="Add",
                   command=add,
                   font=("Helvetica", 10, "bold"),
                   bg="#7a6b85",
                   fg="#ffffff",
                   relief="flat",
                   width=15)
addButton.grid(row=0, column=0, padx=5, pady=5)

deletebutton = Button(frame2,
                      text="Delete",
                      font=("Helvetica", 10, "bold"),
                      bg="#19adb2",
                      fg="#ffffff",
                      relief="flat",
                      width=15,
                      command=delete)
deletebutton.grid(row=0, column=1, padx=5, pady=5)

completebutton = Button(frame2,
                        text="Mark as done",
                        font=("Helvetica", 10, "bold"),
                        bg="#7e6080",
                        fg="#ffffff",
                        relief="flat",
                        width=15,
                        command=complete)
completebutton.grid(row=1, column=0, padx=5, pady=5)

starbutton = Button(frame2,
                    text="Star/Unstar",
                    font=("Helvetica", 10, "bold"),
                    bg="#8a883d",
                    fg="#ffffff",
                    relief="flat",
                    width=15,
                    command=star)
starbutton.grid(row=1, column=1, padx=5, pady=5)

showbutton = Button(frame2,
                    text="Show Starred",
                    font=("Helvetica", 10, "bold"),
                    bg="#246464",
                    fg="#ffffff",
                    relief="flat",
                    width=15,
                    command=showstarred)
showbutton.grid(row=2, column=0, padx=5, pady=5)

completedbutton = Button(frame2,
                         text="Show Completed",
                         font=("Helvetica", 10, "bold"),
                         bg="#929ba4",
                         fg="#ffffff",
                         relief="flat",
                         width=15,
                         command=showcompleted)
completedbutton.grid(row=2, column=1, padx=5, pady=5)
# Add a priority slider with three options
priority_slider = Scale(frame2,
                        from_=0,
                        to=3,
                        orient=HORIZONTAL,
                        length=150,
                        bg="#2f3e45",
                        fg="#ffffff",
                        highlightbackground="#2f3e45",
                        label="Filter by Priority",
                        font=("Helvetica", 10, "bold"),
                        command=lambda value: filter_by_priority(value))
priority_slider.grid(row=4, column=0, columnspan=2, pady=10)
priority_slider.config(tickinterval=1)
priority_slider.set(0)



img = PhotoImage(file="random.png")

image_label = Label(frame2, image=img, bg="#2f3e45")
image_label.grid(row=7, column=0, columnspan=2, pady=10)

# frame for labels entries and other things
frame3 = Frame(frame1, bg="#2f3e45")
frame3.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
# frame for jst entries
frame4 = Frame(frame3, bg="#2f3e45")
frame4.pack(pady=10)
tasklabel = Label(frame4,
                  text="Enter your Task: ",
                  font=("Helvetica", 11),
                  bg="#2f3e45",
                  fg="#ffffff")
tasklabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")
taskEntryBox = Entry(frame4,
                     font=("Helvetica", 11),
                     width=35,
                     relief="solid")
taskEntryBox.grid(row=0, column=1, padx=5, pady=5)
prioritylabel = Label(frame4,
                      text="Enter the Priority: ",
                      font=("Helvetica", 11),
                      bg="#2f3e45",
                      fg="#ffffff"
                      )
prioritylabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
priorityentrybox = Entry(frame4,
                         font=("Helvetica", 11),
                         width=35,
                         relief="solid"
                         )
priorityentrybox.grid(row=1, column=1, padx=5, pady=5)
deadlinelabel = Label(frame4,
                      text="Enter the Deadline: ",
                      font=("Helvetica", 11),
                      bg="#2f3e45",
                      fg="#ffffff"
                      )
deadlinelabel.grid(row=2, column=0, padx=5, pady=5, sticky="w")
deadlineentrybox = Entry(frame4,
                         font=("Helvetica", 11),
                         width=35,
                         relief="solid"
                         )
deadlineentrybox.grid(row=2, column=1, padx=5, pady=5)
# frame for listbox
frame5 = Frame(frame3,
               bg="#2f3e45",
               bd=2,
               relief="solid")
frame5.pack(pady=10, fill="both", expand=True)
listboxtasks = Listbox(frame5,
                       font=("Helvetica", 11),
                       width=60,
                       height=15,
                       bg="#2f3e45",
                       fg="#FFFFFF",
                       relief="flat")
listboxtasks.pack(padx=10, pady=10, fill="both", expand=True)
frame1.columnconfigure(1, weight=1)
frame1.rowconfigure(0, weight=1)

show_starred = False
show_completed = False

tasksLoading()

window.mainloop()