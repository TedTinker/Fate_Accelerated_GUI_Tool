import pygame
import pygame_gui
import json

# Constants for resizing
RESIZE_MARGIN = 10

class CustomWindow:
    def __init__(self, manager, name="name", label="Label", position=(100, 100), size=(300, 200)):
        self.manager = manager
        self.window_rect = pygame.Rect(position, size)
        self.is_minimized = False
        self.is_closed = False
        self.is_dragging = False
        self.is_resizing = False
        self.resize_dir = None
        self.name = name
        self.label = label
        self.create_window_elements()

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
        self.name_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((70, 50), (220, 30)),
                                                            container=self.window_panel,
                                                            manager=self.manager)
        self.name_entry.set_text(self.name)

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.save_button:
                self.save()
            elif event.ui_element == self.close_button:
                self.is_closed = True
                self.window_panel.hide()  # Hide the window panel when closed

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.window_rect.collidepoint(event.pos):
                    if self.is_on_resize_border(event.pos):
                        self.is_resizing = True
                        self.resize_dir = self.get_resize_direction(event.pos)
                    else:
                        self.is_dragging = True
                        self.mouse_offset = (self.window_rect.x - event.pos[0], self.window_rect.y - event.pos[1])

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
                self.is_resizing = False
                self.resize_dir = None

        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.window_rect.topleft = (event.pos[0] + self.mouse_offset[0], event.pos[1] + self.mouse_offset[1])
                self.update_window_position()
            elif self.is_resizing:
                self.resize_window(event.pos)

    def is_on_resize_border(self, pos):
        x, y = pos
        return (
            self.window_rect.left - RESIZE_MARGIN <= x <= self.window_rect.left + RESIZE_MARGIN or
            self.window_rect.right - RESIZE_MARGIN <= x <= self.window_rect.right + RESIZE_MARGIN or
            self.window_rect.top - RESIZE_MARGIN <= y <= self.window_rect.top + RESIZE_MARGIN or
            self.window_rect.bottom - RESIZE_MARGIN <= y <= self.window_rect.bottom + RESIZE_MARGIN
        )

    def get_resize_direction(self, pos):
        x, y = pos
        direction = []
        if self.window_rect.left - RESIZE_MARGIN <= x <= self.window_rect.left + RESIZE_MARGIN:
            direction.append('left')
        if self.window_rect.right - RESIZE_MARGIN <= x <= self.window_rect.right + RESIZE_MARGIN:
            direction.append('right')
        if self.window_rect.top - RESIZE_MARGIN <= y <= self.window_rect.top + RESIZE_MARGIN:
            direction.append('top')
        if self.window_rect.bottom - RESIZE_MARGIN <= y <= self.window_rect.bottom + RESIZE_MARGIN:
            direction.append('bottom')
        return direction

    def resize_window(self, pos):
        x, y = pos
        if 'left' in self.resize_dir:
            new_width = self.window_rect.width - (x - self.window_rect.left)
            if new_width >= 100:
                self.window_rect.width = new_width
                self.window_rect.left = x
        if 'right' in self.resize_dir:
            new_width = x - self.window_rect.left
            if new_width >= 100:
                self.window_rect.width = new_width
        if 'top' in self.resize_dir:
            new_height = self.window_rect.height - (y - self.window_rect.top)
            if new_height >= 100:
                self.window_rect.height = new_height
                self.window_rect.top = y
        if 'bottom' in self.resize_dir:
            new_height = y - self.window_rect.top
            if new_height >= 100:
                self.window_rect.height = new_height
        self.update_window_size()

    def update_window_position(self):
        self.window_panel.set_position(self.window_rect.topleft)

    def update_window_size(self):
        self.window_panel.set_dimensions((self.window_rect.width, self.window_rect.height))

    def save(self):
        data = {'name': self.name_entry.get_text(), 'label': self.label}
        with open(f"saved/{self.name_entry.get_text()}.json", 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_data(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def render(self):
        if not self.is_closed:
            self.window_panel.show()
        else:
            self.window_panel.hide()  # Hide the window panel if the window is closed
