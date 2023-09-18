from GameObject import GameObject
class Wall(GameObject):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)
        self.x = x
        self.y = y
        self.sprite = sprite
        # ... additional properties/methods