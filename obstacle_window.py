import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QMessageBox
from default_window import DefaultWindow, button_style

class ObstacleWindow(DefaultWindow):
    def __init__(self, add_default_rows=True):
        super().__init__()
        self.setWindowTitle('Obstacle Window')

        self.rows_layout = QVBoxLayout()
        self.layout.addLayout(self.rows_layout)

        if add_default_rows:
            self.add_row("Obstacle", "0")
            self.add_row("", "0")
        
        self.new_row_button = QPushButton('New Row', self)
        button_style(self.new_row_button)
        self.new_row_button.clicked.connect(lambda: self.add_row("", "0"))
        self.layout.addWidget(self.new_row_button)

    def add_row(self, agent="Obstacle", score="0"):
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_widget.setLayout(row_layout)

        agent_input = QLineEdit(self)
        agent_input.setText(agent)
        row_layout.addWidget(agent_input)

        score_input = QLineEdit(self)
        score_input.setText(score)
        row_layout.addWidget(score_input)

        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_row(row_widget))
        row_layout.addWidget(remove_button)

        self.rows_layout.addWidget(row_widget)

    def remove_row(self, row_widget):
        self.rows_layout.removeWidget(row_widget)
        row_widget.deleteLater()

    def save_contents(self, suppress_message=False):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, 'Warning', 'Name cannot be empty!')
            return
        
        os.makedirs("saved", exist_ok=True)
        file_path = os.path.join("saved", f"{name}.txt")
        
        with open(file_path, 'w') as file:
            file.write(f"WindowType: ObstacleWindow\n")
            file.write(f"Name: {name}\n")
            for i in range(self.rows_layout.count()):
                row_widget = self.rows_layout.itemAt(i).widget()
                if row_widget:
                    agent_input = row_widget.layout().itemAt(0).widget()
                    score_input = row_widget.layout().itemAt(1).widget()
                    file.write(f"{agent_input.text()}:{score_input.text()}\n")
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {name}.txt')

    def load_contents(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.name_input.setText(lines[1].split(": ")[1].strip())
            for line in lines[2:]:
                agent, score = line.strip().split(':')
                self.add_row(agent, score)
