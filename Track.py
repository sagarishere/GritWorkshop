from GameObject import GameObject
class Track(GameObject):
    def __init__(self, x, y, sprite, sequence_number, array_pos_x, array_pos_y):
        super().__init__(x, y, sprite)
        self.x = x
        self.y = y
        self.sprite = sprite
        self.sequence_number = sequence_number
        self.array_pos_x = array_pos_x
        self.array_pos_y = array_pos_y
        # ... additional properties/methods