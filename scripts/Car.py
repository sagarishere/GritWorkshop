from GameObject import GameObject
import pygame
import math
from Sprite import Sprite
from TemporaryObj import TemporaryObj

class Car(GameObject):

    def __init__(self, x, y, sprite, max_vel, rotation_vel, angle, car_explosion_velocity,AI_CONTROLLED=False):
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
        self.AI_CONTROLLED = AI_CONTROLLED
        self.input_threshold = 0.5  # You can adjust this threshold as per your needs
        self.car_explosion_velocity = car_explosion_velocity

    def get_input(self):
        if self.AI_CONTROLLED:
            ai_output = self.ai_agent.GET_AI_OUTPUT()  # Fetching AI's outputs
            return {
                'left': ai_output[0] > self.input_threshold,
                'right': ai_output[1] > self.input_threshold,
                'forward': ai_output[2] > self.input_threshold,
                'reverse': ai_output[3] > self.input_threshold,  # Reverse movement
                'brake': ai_output[4] > self.input_threshold  # Moved brake to the last index
            }
        else:
            keys = pygame.key.get_pressed()
            return {
                'left': keys[pygame.K_a],
                'right': keys[pygame.K_d],
                'forward': keys[pygame.K_w],
                'reverse': keys[pygame.K_s],  # Reverse movement
                'brake': keys[pygame.K_SPACE]  # Changed brake to SPACE for clarity
            }
        
    def set_ai_agent_controller(self, agent):
        self.ai_agent = agent

    def move_reverse(self):
        reverse_speed = self.max_vel * 0.3
        self.vel = max(self.vel - self.acceleration, -reverse_speed)
        self.move()

    def handle_input(self):
        input_data = self.get_input()

        if input_data['left']:
            self.rotate(left=True)
        if input_data['right']:
            self.rotate(right=True)
        if input_data['forward'] and not input_data['reverse']:
            self.move_forward()
        elif input_data['reverse'] and not input_data['forward']:
            self.move_reverse()
        elif input_data['brake']:  # Brake functionality
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
        
        self.x = min(max(self.x, 0), WIDTH - self.rect.width)
        self.y = min(max(self.y, 0), HEIGHT - self.rect.height)




        # def create_explosion(self, x, y):
        #     # Added explosion to dynamic_gameobjects
        #     explosion_sprite = Sprite("assets/explosion.png")
        #     obj = TemporaryObj(x, y, explosion_sprite, 1)
        #     self.notify_add_gameobject(obj)
