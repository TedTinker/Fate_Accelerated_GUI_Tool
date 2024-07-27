from custom_window import CustomWindow

class CharacterWindow(CustomWindow):
    def __init__(self, manager, name="name", label="Character", position=(100, 100), size=(300, 200)):
        super().__init__(manager, name, label, position, size)
        # Additional initialization for CharacterWindow if needed

class ObstacleWindow(CustomWindow):
    def __init__(self, manager, name="name", label="Obstacle", position=(100, 100), size=(300, 200)):
        super().__init__(manager, name, label, position, size)
        # Additional initialization for ObstacleWindow if needed

class ZoneWindow(CustomWindow):
    def __init__(self, manager, name="name", label="Zone", position=(100, 100), size=(300, 200)):
        super().__init__(manager, name, label, position, size)
        # Additional initialization for ZoneWindow if needed