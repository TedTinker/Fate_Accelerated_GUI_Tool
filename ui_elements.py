import pygame
import pygame_gui

def create_ui_elements(manager):
    new_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                                              text='New',
                                              manager=manager)
    load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 10), (100, 50)),
                                               text='Load',
                                               manager=manager)
    save_all_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((230, 10), (100, 50)),
                                                   text='Save All',
                                                   manager=manager)
    return new_button, load_button, save_all_button