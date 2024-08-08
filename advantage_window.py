import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QMessageBox, QFileDialog, QLabel
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from default_window import DefaultWindow, button_style

class AdvantageWindow(DefaultWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Advantage Window')

        # No additional UI elements needed beyond the name input and notes/image

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
            self.setWindowTitle(f"{name} (Advantage)")
        else:
            self.setWindowTitle('Advantage Window')

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
        
        save_folder = os.path.join("saved", "Advantages")
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, f"{name}.txt")
        
        with open(file_path, 'w') as file:
            file.write(f"WindowType: AdvantageWindow\n")
            file.write(f"Name: {name}\n")
            file.write(f"Notes: {self.notes_input.toPlainText()}\n")
            file.write(f"ImagePath: {self.image_path}\n")
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {file_path}')

    def load_contents(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.name_input.setText(lines[1].split(": ")[1].strip())
            self.notes_input.setPlainText(lines[2].split(": ", 1)[1].strip())
            self.image_path = lines[3].split(": ", 1)[1].strip()
            if self.image_path:
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        self.update_window_title()

    def get_save_folder(self):
        return "Advantages"
