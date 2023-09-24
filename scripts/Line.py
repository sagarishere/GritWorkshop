import pygame
class Line:
    def __init__(self, start, end, color=(255, 0, 0), width=1):
        """
        Initialize a line object.
        
        :param start: Starting point of the line.
        :param end: Ending point of the line.
        :param color: Color of the line.
        :param width: Width/thickness of the line.
        """
        self.start = start
        self.end = end
        self.color = color
        self.width = width

    def draw(self, surface):
        """Draw the line on the provided surface."""
        pygame.draw.line(surface, self.color, self.start, self.end, self.width)