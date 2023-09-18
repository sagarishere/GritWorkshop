import pygame as pg
import math
from SubjectInterface import SubjectInterface

class GameObject(SubjectInterface):
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self._observers = []  # Initialize the observer list



    def SetX(self, x):
        self.x = x
    
    def SetY(self, y):
        self.y = y

    def GetX(self):
        return self.x

    def GetY(self):
        return self.y


    def draw(self, screen):
        self.sprite.blit_rotate_center(screen, (self.x, self.y), 0)

    def collide(self, mask, x=0, y=0):
        car_mask = pg.mask.from_surface(self.sprite.image)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def delete_self(self):
        self.notify_remove_gameobject()