import sys
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem, 
                             QHBoxLayout, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor

# To-do List application in PyQt5. This class creates a GUI for managing to-do tasks.
class ToDoApp(QMainWindow):
    def __init__(self):
        # Initialize the main window and set its title, size, and style sheet.
        super().__init__()
        self.setWindowTitle("To-do List")
        self.setGeometry(100, 100, 450, 650)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            ...
        """)
        
        # Initialize task data
        self.tasks = []
        self.current_filter = "all"  # "all", "today", "completed"
        self.data_file = "tasks.json"
        
        # Load existing tasks
        self.load_tasks()
        
        self.initUI()

    def initUI(self):
        # Central widget and main layout
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)
        self.mainLayout.setSpacing(20)

        # Header with back button and title
        headerLayout = QHBoxLayout()
        self.backButton = QPushButton("<")
        self.backButton.setStyleSheet("font-size: 24px; border: none; background: none; color: #007aff;")
        self.backButton.clicked.connect(self.go_back)
        headerLayout.addWidget(self.backButton)

        headerLabel = QLabel("To-do List")
        headerLabel.setStyleSheet("font-size: 26px; font-weight: bold; color: #333;")
        headerLayout.addWidget(headerLabel)
        headerLayout.addStretch(1) # Pushes the label to the left
        self.mainLayout.addLayout(headerLayout)

        # Task list
        self.taskList = QListWidget()
        self.taskList.itemChanged.connect(self.on_task_changed)
        self.taskList.itemDoubleClicked.connect(self.on_task_double_clicked)
        
        # Load tasks from data
        self.refresh_task_list()

        self.mainLayout.addWidget(self.taskList)

        # Add new task section
        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Add New Task")
        self.taskInput.setObjectName("add_button")
        self.taskInput.returnPressed.connect(self.add_new_task)
        self.mainLayout.addWidget(self.taskInput)
        
        # Add task button with same style as input
        self.addTaskButton = QPushButton("Add New Task")
        self.addTaskButton.setObjectName("add_button")
        self.addTaskButton.clicked.connect(self.add_new_task)
        self.mainLayout.addWidget(self.addTaskButton)

        # Navigation bar
        self.navBarLayout = QHBoxLayout()
        self.navBarLayout.setContentsMargins(0, 10, 0, 0)
        self.navBarLayout.setSpacing(0)
        
        # Navigation buttons with icons and labels
        self.todayBtn = self.create_nav_button("Today", "📍")
        self.allTasksBtn = self.create_nav_button("All Tasks", "📄")
        self.completedBtn = self.create_nav_button("Completed", "✅")
        self.settingsBtn = self.create_nav_button("Settings", "⚙️")
        
        # Connect navigation buttons
        self.todayBtn.clicked.connect(lambda: self.set_filter("today"))
        self.allTasksBtn.clicked.connect(lambda: self.set_filter("all"))
        self.completedBtn.clicked.connect(lambda: self.set_filter("completed"))
        self.settingsBtn.clicked.connect(self.show_settings)
        
        # Set default active button
        self.allTasksBtn.setChecked(True)
        
        self.navBarLayout.addWidget(self.todayBtn)
        self.navBarLayout.addWidget(self.allTasksBtn)
        self.navBarLayout.addWidget(self.completedBtn)
        self.navBarLayout.addWidget(self.settingsBtn)
        
        self.mainLayout.addLayout(self.navBarLayout)

    def add_list_item(self, task_data):
        # Add a new item to the task list.
        item = QListWidgetItem(task_data["text"])
        item.setFont(QFont("Arial", 18))
        item.setSizeHint(QSize(-1, 60)) # Set a minimum height for the item
        
        # Make item checkable
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # type: ignore
        
        # Store task data in the item
        item.setData(Qt.UserRole, task_data)  # type: ignore
        
        if task_data["completed"]:
            item.setCheckState(Qt.Checked)  # type: ignore
            item.setForeground(QColor(128, 128, 128))  # Gray color
            font = item.font()
            font.setStrikeOut(True)
            item.setFont(font)
        else:
            item.setCheckState(Qt.Unchecked)  # type: ignore

        self.taskList.addItem(item)

    def create_nav_button(self, label, icon):
        # Create a navigation button with the given label and icon.
        button = QPushButton(f"{icon}\n{label}")
        button.setObjectName("nav_button")
        button.setCheckable(True)
        button.setStyleSheet("font-size: 14px; text-align: center;")
        return button

    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
            else:
                # Create some default tasks if no file exists
                self.tasks = [
                    {"id": 1, "text": "Grocery Shopping", "completed": True, "created": "2024-01-01", "due": None},
                    {"id": 2, "text": "Finish Report", "completed": False, "created": "2024-01-01", "due": None},
                    {"id": 3, "text": "Call Mom", "completed": True, "created": "2024-01-01", "due": None},
                    {"id": 4, "text": "Gym Workout", "completed": False, "created": "2024-01-01", "due": None},
                    {"id": 5, "text": "Pay Bills", "completed": False, "created": "2024-01-01", "due": None}
                ]
                self.save_tasks()
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []

    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def add_new_task(self):
        """Add a new task to the list"""
        text = self.taskInput.text().strip()
        if text:
            # Create new task
            new_task = {
                "id": max([task["id"] for task in self.tasks], default=0) + 1,
                "text": text,
                "completed": False,
                "created": datetime.now().strftime("%Y-%m-%d"),
                "due": None
            }
            self.tasks.append(new_task)
            self.save_tasks()
            self.taskInput.clear()
            self.refresh_task_list()

    def on_task_changed(self, item):
        """Handle task completion status change"""
        task_data = item.data(Qt.UserRole)  # type: ignore
        if task_data:
            # Update task completion status
            task = None
            for t in self.tasks:
                if t["id"] == task_data["id"]:
                    t["completed"] = (item.checkState() == Qt.Checked)  # type: ignore
                    task = t
                    break
            
            # Update visual appearance
            if task and task["completed"]:
                item.setForeground(QColor(128, 128, 128))
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
            else:
                item.setForeground(QColor(0, 0, 0))
                font = item.font()
                font.setStrikeOut(False)
                item.setFont(font)
            
            self.save_tasks()

    def on_task_double_clicked(self, item):
        """Handle task deletion on double click"""
        task_data = item.data(Qt.UserRole)  # type: ignore
        if task_data:
            reply = QMessageBox.question(self, 'Delete Task', 
                                       f'Are you sure you want to delete "{task_data["text"]}"?',
                                       QMessageBox.Yes | QMessageBox.No, 
                                       QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # Remove task from data
                self.tasks = [task for task in self.tasks if task["id"] != task_data["id"]]
                self.save_tasks()
                self.refresh_task_list()

    def refresh_task_list(self):
        """Refresh the task list based on current filter"""
        self.taskList.clear()
        
        filtered_tasks = self.get_filtered_tasks()
        for task in filtered_tasks:
            self.add_list_item(task)

    def get_filtered_tasks(self):
        """Get tasks based on current filter"""
        if self.current_filter == "completed":
            return [task for task in self.tasks if task["completed"]]
        elif self.current_filter == "today":
            today = datetime.now().strftime("%Y-%m-%d")
            return [task for task in self.tasks if task["created"] == today or task["due"] == today]
        else:  # "all"
            return self.tasks

    def set_filter(self, filter_type):
        """Set the current filter and update UI"""
        self.current_filter = filter_type
        
        # Update button states
        self.todayBtn.setChecked(filter_type == "today")
        self.allTasksBtn.setChecked(filter_type == "all")
        self.completedBtn.setChecked(filter_type == "completed")
        
        # Refresh task list
        self.refresh_task_list()

    def show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(self, "Settings", "Settings feature coming soon!")

    def go_back(self):
        """Handle back button click"""
        QMessageBox.information(self, "Back", "Back button clicked!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())