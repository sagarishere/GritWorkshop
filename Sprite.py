import pygame
from pygame.locals import *

class Sprite:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)

    def get_rect(self, **kwargs):
        return self.image.get_rect(**kwargs)
    
    
    def scale_image(img, factor):
        size = round(img.get_width() * factor), round(img.get_height() * factor)
        return pygame.transform.scale(img, size)


    def blit_rotate_center(self, win, top_left, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=top_left).center)
        win.blit(rotated_image, new_rect.topleft)