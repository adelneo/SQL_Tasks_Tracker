import sqlite3
import datetime
connection = sqlite3.connect('MyDB.db')

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT,
        desc TEXT,
        due_date DATE,
        status TEXT CHECK(status IN ('To Do', 'In Progress', 'Done'))
    )
''')

connection.commit()

cursor.close()
connection.close()

def insert_task():
    connection = sqlite3.connect('mydb.db')
    cursor = connection.cursor()

    try:
        name = input("Enter task name: ")
        desc = input("Enter task description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        status = input("Enter status ('To Do', 'In Progress', 'Done'): ")

        cursor.execute('''
            INSERT INTO tasks (name, desc, due_date, status)
            VALUES (?, ?, ?, ?)
        ''', (name, desc, due_date, status))

        connection.commit()

        print("Task successfully added!")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        cursor.close()
        connection.close()



def edit_task():
    connection = sqlite3.connect('mydb.db')
    cursor = connection.cursor()

    try:
        task_id = int(input("Enter the ID of the task you want to edit: "))
        cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
        task = cursor.fetchone()

        if task:
            print(f"Current task details: {task}")

            new_name = input("Enter new task name: ")
            new_desc = input("Enter new task description: ")
            new_due_date = input("Enter new due date (YYYY-MM-DD): ")
            new_status = input("Enter new status ('To Do', 'In Progress', 'Done'): ")

            cursor.execute('''
                UPDATE tasks
                SET name=?, desc=?, due_date=?, status=?
                WHERE id=?
            ''', (new_name, new_desc, new_due_date, new_status, task_id))

            connection.commit()

            print(f"Task with ID {task_id} successfully updated!")

        else:
            print(f"No task found with ID {task_id}. Please check the ID and try again.")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        cursor.close()
        connection.close()



def filter_tasks():
    connection = sqlite3.connect('mydb.db')
    cursor = connection.cursor()

    try:
        filter_criteria = input("Enter filter criteria ('status' or 'due_date'): ").lower()

        if filter_criteria not in ['status', 'due_date']:
            print("Invalid filter criteria. Please enter 'status' or 'due_date'.")
            return

        filter_value = input(f"Enter {filter_criteria} to filter by: ")

        if filter_criteria == 'status':
            cursor.execute('SELECT * FROM tasks WHERE status=?', (filter_value,))
        elif filter_criteria == 'due_date':
            cursor.execute('SELECT * FROM tasks WHERE due_date=?', (filter_value,))

        filtered_tasks = cursor.fetchall()

        if filtered_tasks:
            print("Filtered tasks:")
            for task in filtered_tasks:
                print(task)
        else:
            print("No tasks found based on the filter criteria.")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        cursor.close()
        connection.close()



def sort_tasks():
    connection = sqlite3.connect('mydb.db')
    cursor = connection.cursor()

    try:
        sort_column = input("Enter the column to sort by: ")

        valid_columns = ['id', 'name', 'desc', 'due_date', 'status']
        if sort_column not in valid_columns:
            print(f"Invalid column. Please enter one of: {', '.join(valid_columns)}")
            return

        cursor.execute(f'SELECT * FROM tasks ORDER BY {sort_column}')

        sorted_tasks = cursor.fetchall()

        if sorted_tasks:
            print(f"Tasks sorted by {sort_column}:")
            for task in sorted_tasks:
                print(task)
        else:
            print("No tasks found.")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        cursor.close()
        connection.close()



def show_startup_menu():
    print("Welcome to the Task Management System!")
    print("1. Insert a new task")
    print("2. Edit an existing task")
    print("3. Sort tasks")
    print("4. Filter tasks")
    print("0. Exit")

def startup_menu():
    while True:
        show_startup_menu()
        choice = input("Enter your choice (0-4): ")

        if choice == '1':
            insert_task()
        elif choice == '2':
            edit_task()
        elif choice == '3':
            sort_tasks()
        elif choice == '4':
            filter_tasks()
        elif choice == '0':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 4.")

if __name__ == "__main__":
    startup_menu()
