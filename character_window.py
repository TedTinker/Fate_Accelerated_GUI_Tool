import pygame_gui
import pygame
import json
from custom_window import CustomWindow

class CharacterWindow(CustomWindow):
    def __init__(self, manager, name="Character", label="Character", position=(100, 100), size=(300, 200)):
        super().__init__(manager, name, label, position, size)
        self.rows = []
        self.additional_rows = []
        self.six_inputs = []  # Initialize six_inputs here
        self.new_aspect_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 90), (100, 30)),
                                                           text="New Aspect",
                                                           container=self.window_panel,
                                                           manager=self.manager)
        self.new_stunt_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 0), (100, 30)),
                                                                      text="New Stunt",
                                                                      container=self.window_panel,
                                                                      manager=self.manager)
        self.add_initial_rows()
        self.add_additional_initial_rows()
        self.update_positions()  # Ensure initial positions are set correctly

    def add_initial_rows(self):
        self.add_row("High Concept", "", removable=False)
        self.add_row("Trouble", "", removable=False)
        self.add_six_text_inputs()

    def add_additional_initial_rows(self):
        for _ in range(3):
            self.add_additional_row()

    def add_six_text_inputs(self):
        labels = ["Careful", "Clever", "Flashy", "Forceful", "Quick", "Sneaky"]
        for i, label in enumerate(labels):
            x_position = 10 + i * 110
            label_element = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x_position, 0), (100, 30)),
                                                        text=label,
                                                        container=self.window_panel,
                                                        manager=self.manager)
            entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((x_position, 30), (100, 30)),
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
        self.update_positions()

    def add_additional_row(self, entry_text=""):
        entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 0), (300, 30)),
                                                    container=self.window_panel,
                                                    manager=self.manager)
        entry.set_text(entry_text)
        
        remove_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 0), (60, 30)),
                                                     text="Remove",
                                                     container=self.window_panel,
                                                     manager=self.manager)
        
        self.additional_rows.append((entry, remove_button))
        self.update_positions()

    def remove_row(self, row_index):
        label, entry, remove_button = self.rows[row_index]
        if label:
            label.kill()
        entry.kill()
        if remove_button:
            remove_button.kill()
        self.rows.pop(row_index)
        self.update_positions()

    def remove_additional_row(self, row_index):
        entry, remove_button = self.additional_rows[row_index]
        entry.kill()
        remove_button.kill()
        self.additional_rows.pop(row_index)
        self.update_positions()

    def update_positions(self):
        for i, (label, entry, remove_button) in enumerate(self.rows):
            y_position = 130 + i * 40
            if label:
                label.set_relative_position((10, y_position))
            entry.set_relative_position((120, y_position))
            if remove_button:
                remove_button.set_relative_position((330, y_position))
        
        six_inputs_y = 130 + len(self.rows) * 40
        for i, (label, entry) in enumerate(self.six_inputs):
            x_position = 10 + i * 110
            label.set_relative_position((x_position, six_inputs_y))
            entry.set_relative_position((x_position, six_inputs_y + 30))
        
        # Correct the position of the "New Stunt" button
        self.new_stunt_button.set_position((110, six_inputs_y + 170))

        additional_rows_y = six_inputs_y + 110  # Adjust this value as needed
        for i, (entry, remove_button) in enumerate(self.additional_rows):
            y_position = additional_rows_y + i * 40
            entry.set_relative_position((10, y_position))
            remove_button.set_relative_position((320, y_position))
            
    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.new_aspect_button:
                self.add_row()
            elif event.ui_element == self.new_stunt_button:
                self.add_additional_row()
            else:
                for i, (_, _, remove_button) in enumerate(self.rows):
                    if remove_button and event.ui_element == remove_button:
                        self.remove_row(i)
                        break
                for i, (entry, remove_button) in enumerate(self.additional_rows):
                    if event.ui_element == remove_button:
                        self.remove_additional_row(i)
                        break

    def save(self):
        data = {
            'name': self.name_entry.get_text(),
            'label': self.label,
            'fate': self.fate_entry.get_text(),  # Save fate value
            'refresh': self.refresh_entry.get_text(),  # Save refresh value
            'rows': [(label.text if label else "", entry.get_text()) for label, entry, _ in self.rows],
            'six_inputs': [entry.get_text() for _, entry in self.six_inputs],
            'additional_rows': [entry.get_text() for entry, _ in self.additional_rows]
        }
        with open(f"saved/{self.name_entry.get_text()}.json", 'w') as f:
            json.dump(data, f)

    def load(self, data):
        self.name_entry.set_text(data['name'])
        self.label = data['label']
        self.fate_entry.set_text(data.get('fate', '3'))  # Load fate value
        self.refresh_entry.set_text(data.get('refresh', '3'))  # Load refresh value
        self.clear_rows()
        for row in data['rows']:
            label_text, entry_text = row
            if label_text in ["High Concept", "Trouble"]:
                self.add_row(label_text, entry_text, removable=False)
            else:
                self.add_row(label_text, entry_text)
        for i, entry_text in enumerate(data['six_inputs']):
            self.six_inputs[i][1].set_text(entry_text)
        self.clear_additional_rows()
        for entry_text in data['additional_rows']:
            self.add_additional_row(entry_text)
        self.update_positions()


    def clear_rows(self):
        while self.rows:
            self.remove_row(0)

    def clear_additional_rows(self):
        while self.additional_rows:
            self.remove_additional_row(0)

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
        for entry, remove_button in self.additional_rows:
            entry.show()
            remove_button.show()
        self.new_aspect_button.show()
        self.new_stunt_button.show()



    def create_window_elements(self):
        self.window_panel = pygame_gui.elements.UIPanel(relative_rect=self.window_rect,
                                                        manager=self.manager)
        self.label_element = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (100, 30)),
                                                        text=self.label,
                                                        container=self.window_panel,
                                                        manager=self.manager)
        self.save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 10), (100, 30)),
                                                        text="Save",
                                                        container=self.window_panel,
                                                        manager=self.manager)
        self.close_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((230, 10), (100, 30)),
                                                        text="Close",
                                                        container=self.window_panel,
                                                        manager=self.manager)
        self.name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 50), (50, 30)),
                                                    text="Name:",
                                                    container=self.window_panel,
                                                    manager=self.manager)
        self.name_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((70, 50), (120, 30)),
                                                            container=self.window_panel,
                                                            manager=self.manager)
        self.name_entry.set_text(self.name)
        
        # Add Fate and Refresh labels and text inputs
        self.fate_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((200, 50), (50, 30)),
                                                    text="Fate:",
                                                    container=self.window_panel,
                                                    manager=self.manager)
        self.fate_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 50), (50, 30)),
                                                            container=self.window_panel,
                                                            manager=self.manager)
        self.fate_entry.set_text("3")
        
        self.refresh_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((310, 50), (70, 30)),
                                                        text="Refresh:",
                                                        container=self.window_panel,
                                                        manager=self.manager)
        self.refresh_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((380, 50), (50, 30)),
                                                                container=self.window_panel,
                                                                manager=self.manager)
        self.refresh_entry.set_text("3")



