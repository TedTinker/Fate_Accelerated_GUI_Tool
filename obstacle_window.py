import pygame_gui
import pygame
import json
from custom_window import CustomWindow

class ObstacleWindow(CustomWindow):
    def __init__(self, manager, name="Obstacle", label="Obstacle", position=(100, 100), size=(300, 200)):
        super().__init__(manager, name, label, position, size)
        self.rows = []
        self.new_row_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 90), (100, 30)),
                                                           text="New Row",
                                                           container=self.window_panel,
                                                           manager=self.manager)
        self.add_initial_rows()

    def add_initial_rows(self):
        self.add_row("Goal", "0")
        self.add_row("Player", "0")

    def add_row(self, player_text="", points_text="0"):
        y_position = 130 + len(self.rows) * 40
        player_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, y_position), (100, 30)),
                                                           container=self.window_panel,
                                                           manager=self.manager)
        player_entry.set_text(player_text)
        
        points_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((120, y_position), (100, 30)),
                                                           container=self.window_panel,
                                                           manager=self.manager)
        points_entry.set_text(points_text)
        
        remove_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((230, y_position), (60, 30)),
                                                     text="Remove",
                                                     container=self.window_panel,
                                                     manager=self.manager)
        
        self.rows.append((player_entry, points_entry, remove_button))

    def remove_row(self, row_index):
        player_entry, points_entry, remove_button = self.rows[row_index]
        player_entry.kill()
        points_entry.kill()
        remove_button.kill()
        self.rows.pop(row_index)
        self.update_rows_positions()

    def update_rows_positions(self):
        for i, (player_entry, points_entry, remove_button) in enumerate(self.rows):
            y_position = 130 + i * 40
            player_entry.set_relative_position((10, y_position))
            points_entry.set_relative_position((120, y_position))
            remove_button.set_relative_position((230, y_position))

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
        data = {
            'name': self.name_entry.get_text(),
            'label': self.label,
            'rows': [(player_entry.get_text(), points_entry.get_text()) for player_entry, points_entry, _ in self.rows]
        }
        with open(f"saved/{self.name_entry.get_text()}.json", 'w') as f:
            json.dump(data, f)

    def load(self, data):
        self.name_entry.set_text(data['name'])
        self.label = data['label']
        self.clear_rows()
        for row in data['rows']:
            self.add_row(row[0], row[1])
        
    def clear_rows(self):
        while self.rows:
            self.remove_row(0)

    def render(self):
        super().render()
        for player_entry, points_entry, remove_button in self.rows:
            player_entry.show()
            points_entry.show()
            remove_button.show()
        self.new_row_button.show()
