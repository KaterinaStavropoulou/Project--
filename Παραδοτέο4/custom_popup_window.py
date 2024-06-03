from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout)
from PyQt5.QtGui import QFont, QIcon

class CustomPopupWindow(QWidget):
    def __init__(self, summary, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PocketGuard")
        self.setWindowIcon(QIcon("images/Screenshot 2024-05-14 213211.png"))
        self.setFixedSize(600, 600)
        self.initUI(summary)

    def initUI(self, summary):
        layout = QVBoxLayout()
        
        top_bar_layout = QHBoxLayout()
        app_name = QLabel("PocketGuard")
        app_name.setFont(QFont("Arial", 22, QFont.Bold))
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(app_name, alignment=Qt.AlignCenter)
        top_bar_layout.addStretch()
        layout.addLayout(top_bar_layout)

        top_bar_widget = QWidget()
        top_bar_widget.setLayout(top_bar_layout)
        top_bar_widget.setStyleSheet("background-color: #6A0DAD;") 
        layout.addWidget(top_bar_widget)


        title_label = QLabel("Summary!")
        title_label.setFont(QFont("Arial", 13, QFont.Bold))
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        summary_text = QTextEdit()
        summary_text.setText(summary)
        summary_text.setReadOnly(True)
        summary_text.setFont(QFont("Arial", 11))
        layout.addWidget(summary_text)

        close_button = QPushButton("Close")
        close_button.setFont(QFont("Arial", 14))
        close_button.setStyleSheet("background-color: gray; color: white; border-radius: 10px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #FFC0CB;")