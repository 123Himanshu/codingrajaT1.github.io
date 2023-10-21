import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, content, priority, due_date):
        self.content = content
        self.priority = priority
        self.due_date = due_date
        self.completed = False

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        self.tasks = []
        self.load_tasks_from_file()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Increase the size of the frame to 1/4 of the screen
        frame_width = screen_width // 2
        frame_height = screen_height // 2
        self.root.geometry(f"{frame_width}x{frame_height}")

        # Change the label text to "Content"
        self.content_label = tk.Label(root, text="Content:")
        self.content_label.grid(row=0, column=0)
        self.content_entry = tk.Entry(root)
        self.content_entry.grid(row=0, column=1)

        self.priority_label = tk.Label(root, text="Priority:")
        self.priority_label.grid(row=1, column=0)
        self.priority_var = tk.StringVar()
        self.priority_var.set("Low")
        self.priority_menu = tk.OptionMenu(root, self.priority_var, "Low", "Medium", "High")
        self.priority_menu.grid(row=1, column=1)

        self.due_date_label = tk.Label(root, text="Due Date:")
        self.due_date_label.grid(row=2, column=0)
        self.due_date_entry = tk.Entry(root)
        self.due_date_entry.grid(row=2, column=1)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=0, columnspan=2)

        # Use grid to make the Listbox expand to the size of the frame
        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE, bg="pink")
        self.task_listbox.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # Configure row and column weights
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Change the button label to "Destroy Task"
        self.destroy_button = tk.Button(root, text="Destroy Task", command=self.remove_task)
        self.destroy_button.grid(row=5, column=0, columnspan=2)

        self.complete_button = tk.Button(root, text="Mark as Completed", command=self.mark_as_completed)
        self.complete_button.grid(row=6, column=0, columnspan=2)

        self.load_tasks_to_listbox()

        # Add a watermark label to the upper screen
        watermark_label = tk.Label(root, text="Task Manager by Himanshu", font=("Helvetica", 12), fg="gray")
        watermark_label.grid(row=0, column=0, columnspan=2, sticky="n")

        root.protocol("WM_DELETE_WINDOW", self.save_tasks_to_file)

    def add_task(self):
        content = self.content_entry.get()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get()
        if content:
            task = Task(content, priority, due_date)
            self.tasks.append(task)
            self.load_tasks_to_listbox()
            self.content_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter content for the task.")

    def remove_task(self):
        selected_task = self.get_selected_task()
        if selected_task:
            self.tasks.remove(selected_task)
            self.load_tasks_to_listbox()

    def mark_as_completed(self):
        selected_task = self.get_selected_task()
        if selected_task:
            selected_task.completed = True
            self.load_tasks_to_listbox()

    def get_selected_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            return self.tasks[int(selected_index[0])]
        return None

    def load_tasks_to_listbox(self):
        self.task_listbox.delete(0, tk.END)

        for i, task in enumerate(self.tasks, start=1):
            status = "Completed" if task.completed else "Incomplete"
            display_text = f"{i}. {task.content} - Priority: {task.priority} - Due Date: {task.due_date} - {status}"
            self.task_listbox.insert(tk.END, display_text)

    def load_tasks_from_file(self):
        try:
            with open('tasks.txt', 'r') as file:
                for line in file:
                    content, priority, due_date, completed = line.strip().split('|')
                    task = Task(content, priority, due_date)
                    task.completed = completed == 'True'
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def save_tasks_to_file(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(f"{task.content}|{task.priority}|{task.due_date}|{task.completed}\n")
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
