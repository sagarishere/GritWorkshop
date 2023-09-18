import pygame
from pygame.locals import *

class Renderer:
    def __init__(self, width=800, height=600, bg_color=(255, 100, 100)):
        pygame.init()
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("2D Racing Game")

    def RenderAllObjects(self, game_objects):
        """
        Draw a list of game objects on the screen.
        :param game_objects: List of GameObject instances.
        """
        # Clear the screen with the background color
        self.screen.fill(self.bg_color)
      #  print(game_objects)
        for x in range(len(game_objects)):
            game_objects[x].draw(self.screen)

        # Update the display
        pygame.display.flip()