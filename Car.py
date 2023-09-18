from GameObject import GameObject
import pygame
import math

class Car(GameObject):

    def __init__(self, x, y, sprite, max_vel, rotation_vel, angle):
        super().__init__(x, y, sprite)
        self.angle = angle
        self.rect = sprite.image.get_rect(topleft=(x, y))
        self.topleft = (x, y)
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.x, self.y = x, y
        self.acceleration = 0.1
        self.prev_x, self.prev_y = x, y  # Store the previous x and y positions


    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(left=True)
        if keys[pygame.K_d]:
            self.rotate(right=True)
        if keys[pygame.K_w]:
            self.move_forward()
        elif keys[pygame.K_s]:  # Brake functionality
            self.brake()
        else:
            self.reduce_speed()

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def update(self):
        self.prev_x, self.prev_y = self.x, self.y  # Store the previous x and y before updating them
        self.handle_input()  # Handle inputs within the update method
        self.keep_on_screen()
        # Any other update logic specific to Car goes here

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def brake(self):
        # Decelerate faster than reduce_speed. Adjust the value as per requirements.
        deceleration_rate = self.acceleration * 3
        self.vel = max(self.vel - deceleration_rate, 0)
        self.move()

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def draw(self, screen):
        self.sprite.blit_rotate_center(screen, (self.x, self.y), self.angle)


    def keep_on_screen(self):
        """Keep the car within screen boundaries."""
        WIDTH = 1536
        HEIGHT = 768
        
        # Check for left boundary
        if self.x < 0:
            self.x = 0

        # Check for right boundary
        if self.x + self.rect.width > WIDTH:
            self.x = WIDTH - self.rect.width

        # Check for top boundary
        if self.y < 0:
            self.y = 0

        # Check for bottom boundary
        if self.y + self.rect.height > HEIGHT:
            self.y = HEIGHT - self.rect.height
