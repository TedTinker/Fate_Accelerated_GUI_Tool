import pygame
import pygame_gui

def create_ui_elements(manager):
    dropdown_menu = pygame_gui.elements.UIDropDownMenu(options_list=['New Character', 'New Obstacle', 'New Zone'],
                                                       starting_option='New Character',
                                                       relative_rect=pygame.Rect((10, 10), (200, 30)),
                                                       manager=manager)
    load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 10), (100, 30)),
                                               text="Load",
                                               manager=manager)
    save_all_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((330, 10), (100, 30)),
                                                   text="Save All",
                                                   manager=manager)
    return dropdown_menu, load_button, save_all_button
