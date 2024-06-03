import os
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout)
from PyQt5.QtGui import QFont
from template import Template
from category_edit import CategoryEditorWindow

CATEGORY_FILE = 'categories.txt'

class CustomizableCategoriesWindow(Template):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PocketGuard - Customizable Categories")
        self.categories = self.load_categories()
        self.initContent()
        self.initMenu()

    def load_categories(self):
        if os.path.exists(CATEGORY_FILE):
            with open(CATEGORY_FILE, 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        return [("Leisure", "Provider 1"), ("Cash", "Provider 2"), ("Health", "Provider 3"), ("Home", "Provider 4"), ("Shopping", "Provider 5"), ("Transport", "Provider 6")]

    def save_categories(self):
        with open(CATEGORY_FILE, 'w') as file:
            for category, provider in self.categories:
                file.write(f"{category}|{provider}\n")

    def initContent(self):
        self.content_layout = QVBoxLayout()

        add_category_label = QLabel("Add New Category")
        add_category_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.content_layout.addWidget(add_category_label, alignment=Qt.AlignCenter)

        self.form_layout = QGridLayout()
        self.form_layout.setHorizontalSpacing(10)
        self.form_layout.setVerticalSpacing(10)
        self.form_layout.setContentsMargins(80, 0, 40, 0)

        self.populate_form()

        self.content_layout.addLayout(self.form_layout)

        add_category_button = QPushButton("Add New Category")
        add_category_button.setFont(QFont("Arial", 16))
        add_category_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        add_category_button.clicked.connect(self.add_new_category)
        self.content_layout.addWidget(add_category_button, alignment=Qt.AlignCenter)

        self.addContent(self.content_layout)

    def populate_form(self):
        for i in reversed(range(self.form_layout.count())):
            item = self.form_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        def add_form_row(row, label_text):
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 16))
            edit_button = QPushButton("Edit")
            edit_button.setFont(QFont("Arial", 14))
            edit_button.setFixedWidth(150)
            edit_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
            edit_button.clicked.connect(lambda _, c=label_text: self.edit_category(c))

            delete_button = QPushButton("Delete")
            delete_button.setFont(QFont("Arial", 14))
            delete_button.setFixedWidth(150)
            delete_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
            delete_button.clicked.connect(lambda _, c=label_text: self.delete_category(c))

            self.form_layout.addWidget(label, row, 0, Qt.AlignLeft)
            button_layout = QHBoxLayout()
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            self.form_layout.addLayout(button_layout, row, 1, Qt.AlignRight)

        for i, (category, _) in enumerate(self.categories):
            add_form_row(i, category)

    def add_new_category(self):
        self.editor_window = CategoryEditorWindow()
        self.editor_window.category_saved.connect(self.add_category)
        self.editor_window.show()

    def edit_category(self, category):
        category_data = next((c, p) for c, p in self.categories if c == category)
        self.editor_window = CategoryEditorWindow(category_data)
        self.editor_window.category_saved.connect(lambda new_category, new_provider: self.update_category(category, new_category, new_provider))
        self.editor_window.show()

    @pyqtSlot(str, str)
    def add_category(self, new_category, new_provider):
        self.categories.append((new_category, new_provider))
        self.save_categories()
        self.populate_form()

    @pyqtSlot(str, str, str)
    def update_category(self, old_category, new_category, new_provider):
        index = next(i for i, (c, p) in enumerate(self.categories) if c == old_category)
        self.categories[index] = (new_category, new_provider)
        self.save_categories()
        self.populate_form()

    def delete_category(self, category):
        self.categories = [(c, p) for c, p in self.categories if c != category]
        self.save_categories()
        self.populate_form()
