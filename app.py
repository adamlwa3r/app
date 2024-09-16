import flet as ft
import json
import os

# File where tasks will be saved
TASKS_FILE = "tasks.json"

class Task(ft.UserControl):

    def __init__(self, input_text, remove_task, completed=False):
        super().__init__()
        self.input_text = input_text
        self.remove_task = remove_task
        self.completed = completed
    
    def build(self):
        # Checkbox with task label
        self.task_cb = ft.Checkbox(label=self.input_text, expand=True, value=self.completed)
        
        # Text field for editing the task
        self.edit_tf = ft.TextField(value=self.input_text, expand=True)
        
        # Row for the task view
        self.task_view = ft.Row(
            visible=True,
            controls=[
                self.task_cb,
                ft.IconButton(icon=ft.icons.CREATE_OUTLINED, on_click=self.edit_clicked),
                ft.IconButton(icon=ft.icons.DELETE_OUTLINE, on_click=self.remove_clicked)
            ]
        )
        
        # Row for the edit view
        self.edit_view = ft.Row(
            visible=False,
            controls=[
                self.edit_tf,
                ft.IconButton(icon=ft.icons.CHECK, on_click=self.save_clicked)
            ]
        )
        
        return ft.Column(controls=[self.task_view, self.edit_view])

    def edit_clicked(self, e):
        # Switch to edit view
        self.task_view.visible = False
        self.edit_view.visible = True
        self.update()

    def remove_clicked(self, e):
        # Call the remove_task method passed from the parent to remove this task
        self.remove_task(self)

    def save_clicked(self, e):
        # Save the edited task and update the task view
        self.task_cb.label = self.edit_tf.value
        self.task_view.visible = True
        self.edit_view.visible = False
        self.update()

    def to_dict(self):
        # Save task details as a dictionary
        return {
            "input_text": self.task_cb.label,
            "completed": self.task_cb.value
        }


class ToDoList(ft.UserControl):
    def build(self):
        # Text field for new task input
        self.input = ft.TextField(hint_text="What should be done?", expand=True)
        
        # Column to hold the tasks
        self.tasks = ft.Column()
        
        # Main view containing the input and tasks
        view = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value="To Do List", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Row(
                    controls=[
                        self.input,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_click)
                    ]
                ),
                self.tasks
            ]
        )

        # Load tasks from file if exists
        self.load_tasks()

        return view

    def add_click(self, e):
        # Add a new task to the list when the "add" button is clicked
        task = Task(self.input.value, self.remove_task)
        self.tasks.controls.append(task)
        self.input.value = ''  # Clear the input field after adding
        self.update()  # Update the UI

    def remove_task(self, task):
        # Remove the specified task from the list
        self.tasks.controls.remove(task)
        self.update()  # Update the UI

    def load_tasks(self):
        # Load tasks from the tasks file
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                tasks_data = json.load(f)
                for task_data in tasks_data:
                    task = Task(task_data["input_text"], self.remove_task, completed=task_data["completed"])
                    self.tasks.controls.append(task)
            self.update()

    def save_tasks(self):
        # Save tasks to the tasks file
        tasks_data = [task.to_dict() for task in self.tasks.controls]
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks_data, f)


def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 600
    page.title = "TO DO List"
    
    # Create and add the ToDoList to the page
    todo_list = ToDoList()
    page.add(todo_list)

    # Save tasks when the page is about to close
    def on_disconnect(e):
        todo_list.save_tasks()

    # Register on_disconnect event to save the tasks on exit
    page.on_disconnect = on_disconnect


# Run the app
ft.app(target=main)
