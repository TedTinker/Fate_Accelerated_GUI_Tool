import pygame_gui
import pygame
import json
from custom_window import CustomWindow

class CharacterWindow(CustomWindow):
    def __init__(self, manager, name="Character", label="Character", position=(100, 100), size=(300, 200)):
        super().__init__(manager, name, label, position, size)
        self.rows = []
        self.new_row_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 90), (100, 30)),
                                                           text="New Row",
                                                           container=self.window_panel,
                                                           manager=self.manager)
        self.add_initial_rows()

    def add_initial_rows(self):
        self.add_row("High Concept", "", removable=False)
        self.add_row("Trouble", "", removable=False)
        self.add_six_text_inputs()

    def add_six_text_inputs(self):
        labels = ["Careful", "Clever", "Flashy", "Forceful", "Quick", "Sneaky"]
        self.six_inputs = []
        for i, label in enumerate(labels):
            x_position = 10 + i * 110
            label_element = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x_position, 210), (100, 30)),
                                                        text=label,
                                                        container=self.window_panel,
                                                        manager=self.manager)
            entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((x_position, 240), (100, 30)),
                                                        container=self.window_panel,
                                                        manager=self.manager)
            entry.set_text("0")
            self.six_inputs.append((label_element, entry))

    def add_row(self, label_text="", entry_text="", removable=True):
        y_position = 130 + len(self.rows) * 40
        if label_text:
            label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, y_position), (100, 30)),
                                                text=label_text,
                                                container=self.window_panel,
                                                manager=self.manager)
        else:
            label = None
        
        entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((120, y_position), (200, 30)),
                                                    container=self.window_panel,
                                                    manager=self.manager)
        entry.set_text(entry_text)
        
        if removable:
            remove_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, y_position), (60, 30)),
                                                         text="Remove",
                                                         container=self.window_panel,
                                                         manager=self.manager)
        else:
            remove_button = None
        
        self.rows.append((label, entry, remove_button))

    def remove_row(self, row_index):
        label, entry, remove_button = self.rows[row_index]
        if label:
            label.kill()
        entry.kill()
        if remove_button:
            remove_button.kill()
        self.rows.pop(row_index)
        self.update_rows_positions()

    def update_rows_positions(self):
        for i, (label, entry, remove_button) in enumerate(self.rows):
            y_position = 130 + i * 40
            if label:
                label.set_relative_position((10, y_position))
            entry.set_relative_position((120, y_position))
            if remove_button:
                remove_button.set_relative_position((330, y_position))

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.new_row_button:
                self.add_row()
            else:
                for i, (_, _, remove_button) in enumerate(self.rows):
                    if remove_button and event.ui_element == remove_button:
                        self.remove_row(i)
                        break

    def save(self):
        data = {
            'name': self.name_entry.get_text(),
            'label': self.label,
            'rows': [(label.text if label else "", entry.get_text()) for label, entry, _ in self.rows],
            'six_inputs': [entry.get_text() for _, entry in self.six_inputs]
        }
        with open(f"saved/{self.name_entry.get_text()}.json", 'w') as f:
            json.dump(data, f)

    def load(self, data):
        self.name_entry.set_text(data['name'])
        self.label = data['label']
        self.clear_rows()
        for row in data['rows']:
            label_text, entry_text = row
            if label_text in ["High Concept", "Trouble"]:
                self.add_row(label_text, entry_text, removable=False)
            else:
                self.add_row(label_text, entry_text)
        for i, entry_text in enumerate(data['six_inputs']):
            self.six_inputs[i][1].set_text(entry_text)

    def clear_rows(self):
        while self.rows:
            self.remove_row(0)

    def render(self):
        super().render()
        for label, entry, remove_button in self.rows:
            if label:
                label.show()
            entry.show()
            if remove_button:
                remove_button.show()
        for label, entry in self.six_inputs:
            label.show()
            entry.show()
        self.new_row_button.show()
