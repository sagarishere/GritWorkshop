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
        elif keys[pygame.K_SPACE]:  # Handbrake functionality
            self.handbrake_turn()
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


    def bounce(self):
        self.vel = -self.vel
        self.move()

    def handbrake_turn(self):
        # Decelerate but not as quickly as a full brake
        deceleration_rate = self.acceleration * 2
        self.vel = max(self.vel - deceleration_rate, 0)

        # Determine the target angle based on current movement direction
        target_angle = self.angle + 180
        target_angle = (target_angle + 360) % 360  # Make sure the angle is between 0 and 360

        # Compute the difference between current angle and target angle
        angle_diff = target_angle - self.angle

        # Determine the shortest rotation direction to the target angle
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360

        # Rotate the car towards the target angle based on a turning rate
        turn_rate = 5  # Adjust this value based on your game's requirements
        rotation_direction = 1 if angle_diff > 0 else -1

        self.angle += rotation_direction * min(abs(angle_diff), turn_rate)
        self.angle = self.angle % 360  # Ensure the angle remains between 0 and 360

        # Continue to move even when turning
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
