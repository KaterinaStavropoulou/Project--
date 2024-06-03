import os
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout)
from PyQt5.QtGui import QFont
from base_window import BaseWindow
from limit_edit import LimitEditorWindow

LIMITS_FILE = 'limits.txt'

class LimitsWindow(BaseWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PocketGuard - Limits")
        self.limits = self.load_limits()
        self.initContent()

    def load_limits(self):
        if os.path.exists(LIMITS_FILE):
            with open(LIMITS_FILE, 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        return [("Leisure", "100"), ("Cash", "200"), ("Health", "300"), ("Home", "400"), ("Shopping", "500"), ("Transport", "600")]

    def save_limits(self):
        with open(LIMITS_FILE, 'w') as file:
            for category, limit in self.limits:
                file.write(f"{category}|{limit}\n")

    def initContent(self):
        self.content_layout = QVBoxLayout()

        # "Add New Limit" label
        add_limit_label = QLabel("Add New Limit")
        add_limit_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.content_layout.addWidget(add_limit_label, alignment=Qt.AlignCenter)

        # Form fields with QGridLayout
        self.form_layout = QGridLayout()
        self.form_layout.setHorizontalSpacing(10)
        self.form_layout.setVerticalSpacing(10)
        self.form_layout.setContentsMargins(40, 0, 40, 0)

        self.populate_form()

        self.content_layout.addLayout(self.form_layout)

        # "Add New Limit" button
        add_limit_button = QPushButton("Add New Limit")
        add_limit_button.setFont(QFont("Arial", 16))
        add_limit_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        add_limit_button.clicked.connect(self.add_new_limit)
        self.content_layout.addWidget(add_limit_button, alignment=Qt.AlignCenter)

        # Add content layout to the main layout
        self.addContent(self.content_layout)

    def populate_form(self):
        for i in reversed(range(self.form_layout.count())):
            item = self.form_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        def add_form_row(row, label_text, limit_text):
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 16))
            limit_label = QLabel(limit_text)
            limit_label.setFont(QFont("Arial", 16))
            
            edit_button = QPushButton("Edit")
            edit_button.setFont(QFont("Arial", 14))
            edit_button.setFixedWidth(150)
            edit_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
            edit_button.clicked.connect(lambda _, c=label_text: self.edit_limit(c))

            delete_button = QPushButton("Delete")
            delete_button.setFont(QFont("Arial", 14))
            delete_button.setFixedWidth(150)
            delete_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
            delete_button.clicked.connect(lambda _, c=label_text: self.delete_limit(c))

            self.form_layout.addWidget(label, row, 0, Qt.AlignLeft)
            self.form_layout.addWidget(limit_label, row, 1, Qt.AlignLeft)
            button_layout = QHBoxLayout()
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            self.form_layout.addLayout(button_layout, row, 2, Qt.AlignRight)

        for i, (category, limit) in enumerate(self.limits):
            add_form_row(i, category, limit)

    def add_new_limit(self):
        self.editor_window = LimitEditorWindow()
        self.editor_window.limit_saved.connect(self.add_limit)
        self.editor_window.show()

    def edit_limit(self, category):
        limit_data = next((c, l) for c, l in self.limits if c == category)
        self.editor_window = LimitEditorWindow(limit_data)
        self.editor_window.limit_saved.connect(lambda new_category, new_limit: self.update_limit(category, new_category, new_limit))
        self.editor_window.show()

    @pyqtSlot(str, str)
    def add_limit(self, new_category, new_limit):
        self.limits.append((new_category, new_limit))
        self.save_limits()
        self.populate_form()

    @pyqtSlot(str, str, str)
    def update_limit(self, old_category, new_category, new_limit):
        index = next(i for i, (c, l) in enumerate(self.limits) if c == old_category)
        self.limits[index] = (new_category, new_limit)
        self.save_limits()
        self.populate_form()

    def delete_limit(self, category):
        self.limits = [(c, l) for c, l in self.limits if c != category]
        self.save_limits()
        self.populate_form()

if __name__ == '__main__':
    app = QApplication([])
    window = LimitsWindow()
    window.show()
    app.exec_()
