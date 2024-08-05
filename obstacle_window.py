import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QPushButton, QWidget, QMessageBox, QLabel
from default_window import DefaultWindow, button_style

class ObstacleWindow(DefaultWindow):
    def __init__(self, add_default_rows=True):
        super().__init__()
        self.setWindowTitle('Obstacle Window')

        # Header layout for labels using QGridLayout
        header_layout = QGridLayout()
        self.layout.insertLayout(1, header_layout)

        header_layout.addWidget(QLabel("Agent"), 0, 0)
        header_layout.addWidget(QLabel("Score"), 0, 1)
        header_layout.addWidget(QLabel(""), 0, 2)

        self.rows_layout = QVBoxLayout()
        self.layout.insertLayout(2, self.rows_layout)

        if add_default_rows:
            self.add_row("Obstacle", "0")
            self.add_row("", "0")
        
        self.new_row_button = QPushButton('New Row', self)
        button_style(self.new_row_button)
        self.new_row_button.clicked.connect(lambda: self.add_row("", "0"))
        self.layout.insertWidget(3, self.new_row_button)

        # Position the toggle button and notes input correctly
        self.layout.addWidget(self.notes_toggle_button)
        self.layout.addWidget(self.notes_input)

    def add_row(self, agent="Obstacle", score="0"):
        row_widget = QWidget()
        row_layout = QGridLayout()
        row_widget.setLayout(row_layout)

        agent_input = QLineEdit(self)
        agent_input.setText(agent)
        row_layout.addWidget(agent_input, 0, 0)

        score_input = QLineEdit(self)
        score_input.setText(score)
        row_layout.addWidget(score_input, 0, 1)

        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_row(row_widget))
        row_layout.addWidget(remove_button, 0, 2)

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
                    agent_input = row_widget.layout().itemAtPosition(0, 0).widget()
                    score_input = row_widget.layout().itemAtPosition(0, 1).widget()
                    file.write(f"{agent_input.text()}:{score_input.text()}\n")
            file.write(f"Notes: {self.notes_input.toPlainText()}\n")
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {name}.txt')

    def load_contents(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.name_input.setText(lines[1].split(": ")[1].strip())
            for line in lines[2:-1]:
                agent, score = line.strip().split(':')
                self.add_row(agent, score)
            self.notes_input.setPlainText(lines[-1].split(": ", 1)[1].strip())
