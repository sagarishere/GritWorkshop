import pygame

class InputHandler:
    def __init__(self):
        self.x_input = 0
        self.y_input = 0

    def update(self):
        keys = pygame.key.get_pressed()
        
        # For X axis: A (left) and D (right)
        if keys[pygame.K_a]:
            self.x_input = -1
        elif keys[pygame.K_d]:
            self.x_input = 1
        else:
            self.x_input = 0
        
        # For Y axis: W (up) and S (down)
        if keys[pygame.K_w]:
            self.y_input = -1
        elif keys[pygame.K_s]:
            self.y_input = 1
        else:
            self.y_input = 0

    def get_x(self):
        return self.x_input

    def get_y(self):
        return self.y_input