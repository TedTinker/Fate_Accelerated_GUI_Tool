import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QMessageBox, QFileDialog, QLabel, QSpinBox
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from default_window import DefaultWindow, button_style

class ObstacleWindow(DefaultWindow):
    def __init__(self, add_default_rows=True):
        super().__init__()
        self.setWindowTitle('Obstacle Window')

        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Agent"))
        header_layout.addWidget(QLabel("Score"))
        header_layout.addWidget(QLabel(""))

        self.layout.addLayout(header_layout)

        self.rows_layout = QVBoxLayout()
        self.layout.addLayout(self.rows_layout)

        if add_default_rows:
            self.add_row("Obstacle", 0)
            self.add_row("", 0)
        
        self.new_row_button = QPushButton('New Row', self)
        button_style(self.new_row_button)
        self.new_row_button.clicked.connect(lambda: self.add_row("", 0))
        self.layout.addWidget(self.new_row_button)

        self.notes_toggle_button.setParent(None)
        self.notes_image_layout.setParent(None)

        self.layout.addWidget(self.notes_toggle_button)
        self.layout.addLayout(self.notes_image_layout)

        self.notes_input.setVisible(True)
        self.image_label.setVisible(True)
        self.choose_image_button.setVisible(True)
        self.notes_toggle_button.setText('Hide Notes and Image')

        self.name_input.textChanged.connect(self.update_window_title)

    def update_window_title(self):
        name = self.name_input.text()
        if name:
            self.setWindowTitle(f"{name} (Obstacle)")
        else:
            self.setWindowTitle('Obstacle Window')

    def add_row(self, agent="Obstacle", score=0):
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_widget.setLayout(row_layout)

        agent_input = QLineEdit(self)
        agent_input.setText(agent)
        row_layout.addWidget(agent_input)

        score_input = QSpinBox(self)
        score_input.setRange(-9999, 9999)
        score_input.setValue(score)
        row_layout.addWidget(score_input)

        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_row(row_widget))
        row_layout.addWidget(remove_button)

        self.rows_layout.addWidget(row_widget)

    def remove_row(self, row_widget):
        self.rows_layout.removeWidget(row_widget)
        row_widget.deleteLater()

    def toggle_notes(self):
        visible = not self.notes_input.isVisible()
        self.notes_input.setVisible(visible)
        self.image_label.setVisible(visible)
        self.choose_image_button.setVisible(visible)
        self.notes_toggle_button.setText('Hide Notes and Image' if visible else 'Show Notes and Image')

    @pyqtSlot()
    def choose_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "pictures", "Image Files (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

    def save_contents(self, suppress_message=False):
        name = self.name_input.text()
        if not name:
            QMessageBox.warning(self, 'Warning', 'Name cannot be empty!')
            return
        
        save_folder = os.path.join("saved", "Obstacles")
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, f"{name}.txt")
        
        with open(file_path, 'w') as file:
            file.write(f"WindowType: ObstacleWindow\n")
            file.write(f"Name: {name}\n")
            for i in range(self.rows_layout.count()):
                row_widget = self.rows_layout.itemAt(i).widget()
                if row_widget:
                    agent_input = row_widget.layout().itemAt(0).widget()
                    score_input = row_widget.layout().itemAt(1).widget()
                    file.write(f"{agent_input.text()}:{score_input.value()}\n")
            notes = self.notes_input.toPlainText().replace('\n', '\\n')
            file.write(f"Notes: {notes}\n")
            file.write(f"ImagePath: {self.image_path}\n")
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {file_path}')

    def load_contents(self, file_path):
        self.clear_rows()

        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.name_input.setText(lines[1].split(": ")[1].strip())
            for line in lines[2:-2]:
                agent, score = line.strip().split(':')
                self.add_row(agent, int(score))
            notes = lines[-2].split(": ", 1)[1].strip().replace('\\n', '\n')
            self.notes_input.setPlainText(notes)
            self.image_path = lines[-1].split(": ", 1)[1].strip()
            if self.image_path:
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

    def clear_rows(self):
        while self.rows_layout.count():
            row = self.rows_layout.takeAt(0)
            if row.widget():
                row.widget().deleteLater()
