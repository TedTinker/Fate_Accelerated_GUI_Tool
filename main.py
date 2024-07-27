#%%
import pygame
import pygame_gui
import os
from custom_window import CustomWindow
from file_utils import select_files
from ui_elements import create_ui_elements
from character_window import CharacterWindow
from obstacle_window import ObstacleWindow
from zone_window import ZoneWindow


pygame.init()

# Screen setup
window_surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Pygame GUI Example')

manager = pygame_gui.UIManager((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

# Create UI elements
dropdown_menu, load_button, save_all_button = create_ui_elements(manager)

# Create the directory for saved windows
os.makedirs("saved", exist_ok=True)

# Initial window position and offset for new windows
initial_window_position = (100, 100)
window_offset = 20

windows = []

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
            
            
        if event.type == pygame.VIDEORESIZE:
            window_surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            background = pygame.Surface((event.w, event.h))
            background.fill(pygame.Color('#000000'))
            manager.set_window_resolution((event.w, event.h))
            
            
            
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == dropdown_menu:
                label = event.text.replace('New ', '')
                if label == 'Character':
                    windows.append(CharacterWindow(manager, label=label,
                                                position=(initial_window_position[0] + len(windows) * window_offset,
                                                            initial_window_position[1] + len(windows) * window_offset)))
                elif label == 'Obstacle':
                    windows.append(ObstacleWindow(manager, label=label,
                                                position=(initial_window_position[0] + len(windows) * window_offset,
                                                            initial_window_position[1] + len(windows) * window_offset)))
                elif label == 'Zone':
                    windows.append(ZoneWindow(manager, label=label,
                                            position=(initial_window_position[0] + len(windows) * window_offset,
                                                        initial_window_position[1] + len(windows) * window_offset)))
                
                
                
                
                
                
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == load_button:
                file_paths = select_files()
                for i, file_path in enumerate(file_paths):
                    data = CustomWindow.load_data(file_path)
                    label = data.get('label', 'Label')
                    if label == 'Character':
                        windows.append(CharacterWindow(manager, name=data.get('name', 'name'),
                                                    position=(initial_window_position[0] + (len(windows) + i) * window_offset,
                                                                initial_window_position[1] + (len(windows) + i) * window_offset),
                                                    label=data.get('label', 'Character')))
                    elif label == 'Obstacle':
                        windows.append(ObstacleWindow(manager, name=data.get('name', 'name'),
                                                position=(initial_window_position[0] + (len(windows) + i) * window_offset,
                                                        initial_window_position[1] + (len(windows) + i) * window_offset),
                                                label=data.get('label', 'Obstacle')))
                    elif label == 'Zone':
                        windows.append(ZoneWindow(manager, name=data.get('name', 'name'),
                                                position=(initial_window_position[0] + (len(windows) + i) * window_offset,
                                                            initial_window_position[1] + (len(windows) + i) * window_offset),
                                                label=data.get('label', 'Zone')))
            
            elif event.ui_element == save_all_button:
                for window in windows:
                    if not window.is_closed:
                        window.save()

        for window in windows:
            window.handle_event(event)

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()

# %%
