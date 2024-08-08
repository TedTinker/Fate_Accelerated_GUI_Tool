import os
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFileDialog, QSpinBox, QCheckBox, QDialog, QDialogButtonBox, QFormLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSlot
from default_window import DefaultWindow, button_style

class CustomDialog(QDialog):
    def __init__(self, title, current_values, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        
        self.layout = QVBoxLayout(self)
        
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)
        
        self.spin_boxes = []
        for value in current_values:
            self.add_spin_box(value)
        
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(lambda: self.add_spin_box(1))
        self.layout.addWidget(self.add_button)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)
    
    def add_spin_box(self, value):
        row_layout = QHBoxLayout()
        spin_box = QSpinBox(self)
        spin_box.setValue(value)
        spin_box.setRange(1, 1000)
        remove_button = QPushButton("Remove", self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_spin_box(row_layout, spin_box))
        
        row_layout.addWidget(spin_box)
        row_layout.addWidget(remove_button)
        self.spin_boxes.append((spin_box, row_layout))
        self.form_layout.addRow(f"Value {len(self.spin_boxes)}:", row_layout)

    def remove_spin_box(self, row_layout, spin_box):
        self.spin_boxes = [(sb, rl) for sb, rl in self.spin_boxes if sb != spin_box]
        for i in reversed(range(row_layout.count())):
            row_layout.itemAt(i).widget().setParent(None)
        self.form_layout.removeRow(row_layout)
    
    def get_values(self):
        return sorted([spin_box.value() for spin_box, _ in self.spin_boxes])

class CharacterWindow(DefaultWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Character Window')

        # Fate Points and Refresh
        fate_refresh_layout = QHBoxLayout()
        self.layout.addLayout(fate_refresh_layout)
        
        fate_refresh_layout.addWidget(QLabel('Fate Points'))
        self.fate_points_input = QSpinBox(self)
        self.fate_points_input.setValue(3)
        self.fate_points_input.setRange(0, 1000)
        fate_refresh_layout.addWidget(self.fate_points_input)
        
        fate_refresh_layout.addWidget(QLabel('Refresh'))
        self.refresh_input = QSpinBox(self)
        self.refresh_input.setValue(3)
        self.refresh_input.setRange(0, 1000)
        fate_refresh_layout.addWidget(self.refresh_input)
        
        # Approaches
        skills_layout = QVBoxLayout()
        self.layout.addLayout(skills_layout)
        
        skills_header_layout = QHBoxLayout()
        skills_layout.addLayout(skills_header_layout)
        
        skills_header_layout.addWidget(QLabel('Careful'))
        skills_header_layout.addWidget(QLabel('Clever'))
        skills_header_layout.addWidget(QLabel('Flashy'))
        skills_header_layout.addWidget(QLabel('Forceful'))
        skills_header_layout.addWidget(QLabel('Quick'))
        skills_header_layout.addWidget(QLabel('Sneaky'))
        
        skills_inputs_layout = QHBoxLayout()
        skills_layout.addLayout(skills_inputs_layout)
        
        self.careful_input = QSpinBox(self)
        skills_inputs_layout.addWidget(self.careful_input)
        
        self.clever_input = QSpinBox(self)
        skills_inputs_layout.addWidget(self.clever_input)
        
        self.flashy_input = QSpinBox(self)
        skills_inputs_layout.addWidget(self.flashy_input)
        
        self.forceful_input = QSpinBox(self)
        skills_inputs_layout.addWidget(self.forceful_input)
        
        self.quick_input = QSpinBox(self)
        skills_inputs_layout.addWidget(self.quick_input)
        
        self.sneaky_input = QSpinBox(self)
        skills_inputs_layout.addWidget(self.sneaky_input)
        
        # Aspects
        aspects_layout = QVBoxLayout()
        self.layout.addLayout(aspects_layout)
        
        aspects_layout.addWidget(QLabel('Aspects:'))
        
        high_concept_layout = QHBoxLayout()
        aspects_layout.addLayout(high_concept_layout)
        high_concept_layout.addWidget(QLabel('High Concept'))
        self.high_concept_input = QLineEdit(self)
        high_concept_layout.addWidget(self.high_concept_input)
        
        trouble_layout = QHBoxLayout()
        aspects_layout.addLayout(trouble_layout)
        trouble_layout.addWidget(QLabel('Trouble'))
        self.trouble_input = QLineEdit(self)
        trouble_layout.addWidget(self.trouble_input)

        self.aspects_list_layout = QVBoxLayout()
        aspects_layout.addLayout(self.aspects_list_layout)
        
        self.add_aspect_button = QPushButton('New Aspect', self)
        button_style(self.add_aspect_button)
        self.add_aspect_button.clicked.connect(self.add_aspect)
        aspects_layout.addWidget(self.add_aspect_button)
        
        # Stunts
        stunts_layout = QVBoxLayout()
        self.layout.addLayout(stunts_layout)
        
        stunts_layout.addWidget(QLabel('Stunts:'))
        
        self.stunts_list_layout = QVBoxLayout()
        stunts_layout.addLayout(self.stunts_list_layout)
        
        self.add_stunt_button = QPushButton('New Stunt', self)
        button_style(self.add_stunt_button)
        self.add_stunt_button.clicked.connect(self.add_stunt)
        stunts_layout.addWidget(self.add_stunt_button)

        # Stress and Consequences
        self.stress_layout = QHBoxLayout()
        self.layout.addLayout(self.stress_layout)
        self.stress_values = [1, 2, 3]
        self.add_stress_row()

        self.consequences_layout = QHBoxLayout()
        self.layout.addLayout(self.consequences_layout)
        self.consequences_values = [2, 4, 6]
        self.add_consequences_row()
        
        self.notes_toggle_button.setParent(None)
        self.notes_image_layout.setParent(None)

        self.layout.addWidget(self.notes_toggle_button)
        self.layout.addLayout(self.notes_image_layout)

        self.notes_input.setVisible(True)
        self.image_label.setVisible(True)
        self.choose_image_button.setVisible(True)
        self.notes_toggle_button.setText('Hide Notes and Image')

    def add_stress_row(self):
        self.clear_layout(self.stress_layout)
        self.stress_layout.addWidget(QLabel('Stress:'))
        self.stress_checkboxes = []
        for value in self.stress_values:
            self.stress_layout.addWidget(QLabel(str(value)))
            checkbox = QCheckBox(self)
            self.stress_checkboxes.append(checkbox)
            self.stress_layout.addWidget(checkbox)
        customize_button = QPushButton('Customize', self)
        button_style(customize_button)
        customize_button.clicked.connect(self.customize_stress)
        self.stress_layout.addWidget(customize_button)

    def add_consequences_row(self):
        self.clear_layout(self.consequences_layout)
        self.consequences_layout.addWidget(QLabel('Consequences:'))
        self.consequences_checkboxes = []
        for value in self.consequences_values:
            self.consequences_layout.addWidget(QLabel(str(value)))
            checkbox = QCheckBox(self)
            self.consequences_checkboxes.append(checkbox)
            self.consequences_layout.addWidget(checkbox)
        customize_button = QPushButton('Customize', self)
        button_style(customize_button)
        customize_button.clicked.connect(self.customize_consequences)
        self.consequences_layout.addWidget(customize_button)

    def customize_stress(self):
        dialog = CustomDialog('Customize Stress', self.stress_values, self)
        if dialog.exec_():
            self.stress_values = dialog.get_values()
            self.add_stress_row()

    def customize_consequences(self):
        dialog = CustomDialog('Customize Consequences', self.consequences_values, self)
        if dialog.exec_():
            self.consequences_values = dialog.get_values()
            self.add_consequences_row()

    def add_aspect(self):
        aspect_layout = QHBoxLayout()
        
        aspect_input = QLineEdit(self)
        aspect_layout.addWidget(aspect_input)
        
        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_aspect(aspect_layout))
        aspect_layout.addWidget(remove_button)
        
        self.aspects_list_layout.addLayout(aspect_layout)
    
    def remove_aspect(self, aspect_layout):
        for i in reversed(range(aspect_layout.count())):
            widget = aspect_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.aspects_list_layout.removeItem(aspect_layout)
    
    def add_stunt(self):
        stunt_layout = QHBoxLayout()
        
        stunt_input = QLineEdit(self)
        stunt_layout.addWidget(stunt_input)
        
        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_stunt(stunt_layout))
        stunt_layout.addWidget(remove_button)
        
        self.stunts_list_layout.addLayout(stunt_layout)
    
    def remove_stunt(self, stunt_layout):
        for i in reversed(range(stunt_layout.count())):
            widget = stunt_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.stunts_list_layout.removeItem(stunt_layout)

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
        
        save_folder = os.path.join("saved", "Characters")
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, f"{name}.txt")
        
        with open(file_path, 'w') as file:
            file.write(f"WindowType: CharacterWindow\n")
            file.write(f"Name: {name}\n")
            file.write(f"Fate Points: {self.fate_points_input.value()}\n")
            file.write(f"Refresh: {self.refresh_input.value()}\n")
            file.write(f"Careful: {self.careful_input.value()}\n")
            file.write(f"Clever: {self.clever_input.value()}\n")
            file.write(f"Flashy: {self.flashy_input.value()}\n")
            file.write(f"Forceful: {self.forceful_input.value()}\n")
            file.write(f"Quick: {self.quick_input.value()}\n")
            file.write(f"Sneaky: {self.sneaky_input.value()}\n")
            
            file.write(f"High Concept: {self.high_concept_input.text()}\n")
            file.write(f"Trouble: {self.trouble_input.text()}\n")
            
            for i in range(self.aspects_list_layout.count()):
                aspect_layout = self.aspects_list_layout.itemAt(i).layout()
                if aspect_layout:
                    aspect_input = aspect_layout.itemAt(0).widget()
                    file.write(f"Aspect: {aspect_input.text()}\n")
            
            for i in range(self.stunts_list_layout.count()):
                stunt_layout = self.stunts_list_layout.itemAt(i).layout()
                if stunt_layout:
                    stunt_input = stunt_layout.itemAt(0).widget()
                    file.write(f"Stunt: {stunt_input.text()}\n")

            file.write(f"Stress: {' '.join(str(value) for value in self.stress_values)}\n")
            file.write(f"StressCheckboxes: {' '.join('1' if cb.isChecked() else '0' for cb in self.stress_checkboxes)}\n")
            file.write(f"Consequences: {' '.join(str(value) for value in self.consequences_values)}\n")
            file.write(f"ConsequencesCheckboxes: {' '.join('1' if cb.isChecked() else '0' for cb in self.consequences_checkboxes)}\n")

            file.write(f"Notes: {self.notes_input.toPlainText()}\n")
            file.write(f"ImagePath: {self.image_path}\n")
        
        if not suppress_message:
            QMessageBox.information(self, 'Info', f'Contents saved to {file_path}')

    def load_contents(self, file_path):
        self.clear_layout(self.aspects_list_layout)
        self.clear_layout(self.stunts_list_layout)
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.name_input.setText(lines[1].split(": ")[1].strip())
            self.fate_points_input.setValue(int(lines[2].split(": ")[1].strip()))
            self.refresh_input.setValue(int(lines[3].split(": ")[1].strip()))
            self.careful_input.setValue(int(lines[4].split(": ")[1].strip()))
            self.clever_input.setValue(int(lines[5].split(": ")[1].strip()))
            self.flashy_input.setValue(int(lines[6].split(": ")[1].strip()))
            self.forceful_input.setValue(int(lines[7].split(": ")[1].strip()))
            self.quick_input.setValue(int(lines[8].split(": ")[1].strip()))
            self.sneaky_input.setValue(int(lines[9].split(": ")[1].strip()))
            self.high_concept_input.setText(lines[10].split(": ")[1].strip())
            self.trouble_input.setText(lines[11].split(": ")[1].strip())
            
            line_index = 12
            for line in lines[12:]:
                if line.startswith("Aspect:"):
                    aspect_text = line.split(": ")[1].strip()
                    self.add_aspect_with_text(aspect_text)
                    line_index += 1
                elif line.startswith("Stunt:"):
                    stunt_text = line.split(": ")[1].strip()
                    self.add_stunt_with_text(stunt_text)
                    line_index += 1
                else:
                    break

            stress_line = lines[line_index].split(": ")[1].strip().split()
            self.stress_values = [int(value) for value in stress_line]
            self.add_stress_row()
            line_index += 1
            
            stress_checkboxes_line = lines[line_index].split(": ")[1].strip().split()
            for i, cb_value in enumerate(stress_checkboxes_line):
                self.stress_checkboxes[i].setChecked(cb_value == '1')
            line_index += 1

            consequences_line = lines[line_index].split(": ")[1].strip().split()
            self.consequences_values = [int(value) for value in consequences_line]
            self.add_consequences_row()
            line_index += 1
            
            consequences_checkboxes_line = lines[line_index].split(": ")[1].strip().split()
            for i, cb_value in enumerate(consequences_checkboxes_line):
                self.consequences_checkboxes[i].setChecked(cb_value == '1')
            line_index += 1

            self.notes_input.setPlainText(lines[line_index].split(": ", 1)[1].strip())
            self.image_path = lines[line_index + 1].split(": ", 1)[1].strip()
            if self.image_path:
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def add_aspect_with_text(self, text):
        aspect_layout = QHBoxLayout()
        
        aspect_input = QLineEdit(self)
        aspect_input.setText(text)
        aspect_layout.addWidget(aspect_input)
        
        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_aspect(aspect_layout))
        aspect_layout.addWidget(remove_button)
        
        self.aspects_list_layout.addLayout(aspect_layout)

    def add_stunt_with_text(self, text):
        stunt_layout = QHBoxLayout()
        
        stunt_input = QLineEdit(self)
        stunt_input.setText(text)
        stunt_layout.addWidget(stunt_input)
        
        remove_button = QPushButton('Remove', self)
        button_style(remove_button)
        remove_button.clicked.connect(lambda: self.remove_stunt(stunt_layout))
        stunt_layout.addWidget(remove_button)
        
        self.stunts_list_layout.addLayout(stunt_layout)
