from custom_window import CustomWindow
import pygame_gui
import pygame
import json

class ObstacleWindow(CustomWindow):
    def __init__(self, manager, name="Obstacle", label="Obstacle", position=(100, 100), size=(300, 200)):
        super().__init__(manager, name, label, position, size)
        self.rows = []
        self.new_row_button = None
        self.init_obstacle_window()

    def init_obstacle_window(self):
        self.add_row("Goal", "0")
        self.add_row("Player", "0")
        self.new_row_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 210), (100, 30)),
                                                           text="New Row",
                                                           container=self.window_panel,
                                                           manager=self.manager)
    
    def add_row(self, text1="", text2="0"):
        y_offset = 90 + len(self.rows) * 40
        text_entry1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, y_offset), (100, 30)),
                                                          container=self.window_panel,
                                                          manager=self.manager)
        text_entry1.set_text(text1)
        text_entry2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((120, y_offset), (100, 30)),
                                                          container=self.window_panel,
                                                          manager=self.manager)
        text_entry2.set_text(text2)
        remove_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((230, y_offset), (60, 30)),
                                                     text="Remove",
                                                     container=self.window_panel,
                                                     manager=self.manager)
        self.rows.append((text_entry1, text_entry2, remove_button))
        self.reposition_rows()  # Reposition rows and the new row button after adding a new row
    
    def remove_row(self, index):
        text_entry1, text_entry2, remove_button = self.rows.pop(index)
        text_entry1.kill()
        text_entry2.kill()
        remove_button.kill()
        self.reposition_rows()

    def reposition_rows(self):
        for i, (text_entry1, text_entry2, remove_button) in enumerate(self.rows):
            y_offset = 90 + i * 40
            text_entry1.set_position((10, y_offset))
            text_entry2.set_position((120, y_offset))
            remove_button.set_position((230, y_offset))
        if self.new_row_button:
            self.new_row_button.set_position((10, 90 + len(self.rows) * 40 + 10))
    
    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.new_row_button:
                self.add_row()
            else:
                for i, (_, _, remove_button) in enumerate(self.rows):
                    if event.ui_element == remove_button:
                        self.remove_row(i)
                        break

    def save(self):
        data = {'name': self.name_entry.get_text(), 'label': self.label, 'rows': []}
        for text_entry1, text_entry2, _ in self.rows:
            data['rows'].append({'text1': text_entry1.get_text(), 'text2': text_entry2.get_text()})
        with open(f"saved/{self.name_entry.get_text()}.json", 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_data(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def load(self, data):
        for text_entry1, text_entry2, remove_button in self.rows:
            text_entry1.kill()
            text_entry2.kill()
            remove_button.kill()
        self.rows.clear()
        for row in data.get('rows', []):
            self.add_row(row.get('text1', ''), row.get('text2', '0'))
        self.reposition_rows()
