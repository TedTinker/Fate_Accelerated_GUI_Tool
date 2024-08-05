import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QAction, QMdiArea, QMdiSubWindow
from PyQt5.QtCore import Qt

from default_window import DefaultWindow
from character_window import CharacterWindow
from obstacle_window import ObstacleWindow
from zone_window import ZoneWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 800, 600)
        
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        
        self.create_menu()
        
    def create_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('File')
        
        new_character_action = QAction('New Character Window', self)
        new_character_action.triggered.connect(lambda: self.new_window(CharacterWindow))
        file_menu.addAction(new_character_action)
        
        new_obstacle_action = QAction('New Obstacle Window', self)
        new_obstacle_action.triggered.connect(lambda: self.new_window(ObstacleWindow))
        file_menu.addAction(new_obstacle_action)
        
        new_zone_action = QAction('New Zone Window', self)
        new_zone_action.triggered.connect(lambda: self.new_window(lambda: ZoneWindow(self.mdi_area)))
        file_menu.addAction(new_zone_action)
        
        load_action = QAction('Load', self)
        load_action.triggered.connect(self.load_windows)
        file_menu.addAction(load_action)

        save_all_action = QAction('Save All', self)
        save_all_action.triggered.connect(self.save_all_windows)
        file_menu.addAction(save_all_action)
        
        close_all_action = QAction('Close All', self)
        close_all_action.triggered.connect(self.close_all_windows)
        file_menu.addAction(close_all_action)
    
    def new_window(self, window_class):
        sub_window = QMdiSubWindow()
        window_instance = window_class()
        sub_window.setWidget(window_instance)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
        
        self.update_zone_window_dropdowns()

    def load_windows(self):
        options = QFileDialog.Options()
        file_names, _ = QFileDialog.getOpenFileNames(self, "Load Files", "saved", "Text Files (*.txt);;All Files (*)", options=options)
        if file_names:
            for file_name in file_names:
                with open(file_name, 'r') as file:
                    first_line = file.readline()
                    window_type = first_line.split(": ")[1].strip()
                    
                    sub_window = QMdiSubWindow()
                    
                    if window_type == "ObstacleWindow":
                        window_instance = ObstacleWindow(add_default_rows=False)
                    elif window_type == "CharacterWindow":
                        window_instance = CharacterWindow()
                    elif window_type == "ZoneWindow":
                        window_instance = ZoneWindow(self.mdi_area)
                    else:
                        window_instance = DefaultWindow()

                    window_instance.load_contents(file_name)  # Ensure the load_contents method is called
                    sub_window.setWidget(window_instance)
                    sub_window.setAttribute(Qt.WA_DeleteOnClose)
                    self.mdi_area.addSubWindow(sub_window)
                    sub_window.show()
        
        self.update_zone_window_dropdowns()

    def save_all_windows(self):
        saved_files = []
        for sub_window in self.mdi_area.subWindowList():
            widget = sub_window.widget()
            if isinstance(widget, DefaultWindow):
                name = widget.name_input.text()
                if name:
                    widget.save_contents(suppress_message=True)
                    saved_files.append(f"{name}.txt")
        
        if saved_files:
            saved_files_str = ", ".join(saved_files)
            QMessageBox.information(self, 'Info', f'Contents saved to {saved_files_str}')
                
    def close_all_windows(self):
        for sub_window in self.mdi_area.subWindowList():
            sub_window.close()
        
        self.update_zone_window_dropdowns()

    def update_zone_window_dropdowns(self):
        for sub_window in self.mdi_area.subWindowList():
            if isinstance(sub_window.widget(), ZoneWindow):
                sub_window.widget().update_dropdown()
