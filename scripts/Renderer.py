import pygame
from pygame.locals import *

class Renderer:
    class TextObject:
        def __init__(self, font_name=None, font_size=32, font_color=(255, 255, 255), pos=None, center=False):
            pygame.font.init()  # Ensure the pygame font system is initialized
            self.font = pygame.font.Font(font_name, font_size)  # None means use the default pygame font
            self.color = font_color
            self.center = center  # A flag to indicate if the text should be centered on the screen
            self.pos = pos
            self.text_surface = None  # Placeholder for the rendered text surface

        def update_text(self, text, width, height):
            """Update the text without drawing it."""
            self.text_surface = self.font.render(text, True, self.color)  # Render the text
            
            # If we want to center the text, recalculate the position based on the text's width and height
            if self.center:
                self.pos = ((width - self.text_surface.get_width()) // 2, 
                            (height - self.text_surface.get_height()) // 2)
            elif self.pos is None:
                self.pos = (0, 0)  # Default to top-left if no position is provided

        def draw(self, screen):
            """Draw the rendered text on the specified screen."""
            if self.text_surface:
                screen.blit(self.text_surface, self.pos)

    def __init__(self, width=800, height=600, bg_color=(255, 100, 100)):
        pygame.init()
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("2D Racing Game")
        self.text_objects = []

    def RenderAllObjects(self, game_objects):
        """Draw a list of game objects on the screen."""
        # Clear the screen with the background color
        self.screen.fill(self.bg_color)
        for obj in game_objects:
            obj.draw(self.screen)

    def RenderAllButtons(self, buttons):
        """Draw all buttons."""
        for button in buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def RenderAllLines(self, lines):
        """Draw all line objects."""
        for line_obj in lines:
            line_obj.draw(self.screen)


    def RenderAllTextObjects(self):
        """Draw all text objects."""
        for text_obj in self.text_objects:
            text_obj.draw(self.screen)
        # Update the display
