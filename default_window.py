import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSlot



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
        self.save_button.clicked.connect(self.save_contents)
        self.name_layout.addWidget(self.save_button)
        
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
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {name}.txt')
