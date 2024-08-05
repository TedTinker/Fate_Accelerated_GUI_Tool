import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QTextEdit
from PyQt5.QtCore import pyqtSlot

def button_style(button):
    button.setStyleSheet("background-color: #888888; color: white;")

class DefaultWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Default Window')
        self.setGeometry(100, 100, 400, 200)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.name_layout = QHBoxLayout()
        self.layout.addLayout(self.name_layout)
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Name')
        self.name_layout.addWidget(self.name_input)
        
        self.save_button = QPushButton('Save', self)
        button_style(self.save_button)
        self.save_button.clicked.connect(self.save_contents)
        self.name_layout.addWidget(self.save_button)
        
        # Notes section with toggle button
        self.notes_toggle_button = QPushButton('Show Notes', self)
        button_style(self.notes_toggle_button)
        self.notes_toggle_button.clicked.connect(self.toggle_notes)
        self.layout.addWidget(self.notes_toggle_button)
        
        self.notes_input = QTextEdit(self)
        self.notes_input.setPlaceholderText('Notes')
        self.notes_input.setVisible(False)  # Initially hidden
        self.layout.addWidget(self.notes_input)
        
    def toggle_notes(self):
        if self.notes_input.isVisible():
            self.notes_input.setVisible(False)
            self.notes_toggle_button.setText('Show Notes')
        else:
            self.notes_input.setVisible(True)
            self.notes_toggle_button.setText('Hide Notes')
        
    @pyqtSlot()
    def save_contents(self, suppress_message=False):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, 'Warning', 'Name cannot be empty!')
            return
        
        os.makedirs("saved", exist_ok=True)
        file_path = os.path.join("saved", f"{name}.txt")
        
        with open(file_path, 'w') as file:
            file.write(f"Name: {name}\n")
            file.write(f"Notes: {self.notes_input.toPlainText()}\n")
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {name}.txt')
    
    def load_contents(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.name_input.setText(lines[0].split(": ")[1].strip())
            self.notes_input.setPlainText(lines[1].split(": ", 1)[1].strip())
