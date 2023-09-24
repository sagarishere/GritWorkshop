

import math
from Wall import Wall
from Track import Track
from Car import Car
from FinishLine import FinishLine
import time


def check_collisions(dynamic_gameobjects, spatial_grid, race_progress, race_lenght):
        
        for x in range(len(dynamic_gameobjects)):
            car = dynamic_gameobjects[x]
            neighboring_objects = spatial_grid.get_neighboring_objects(car.x, car.y)
            
            for obj in neighboring_objects:
                if isinstance(obj, Wall):
                    if car.sprite.get_rect(topleft=(car.x, car.y)).colliderect(obj.sprite.get_rect(topleft=(obj.x, obj.y))):
                        dx = car.rect.centerx - obj.sprite.get_rect().centerx
                        dy = car.rect.centery - obj.sprite.get_rect().centery
                        collision_angle = math.atan2(dy, dx)
                        car_angle_radians = math.radians(car.angle)

                        angle_difference = abs(car_angle_radians - collision_angle)
                        if angle_difference > math.pi:
                            angle_difference = 2 * math.pi - angle_difference

                        if car.vel > car.car_explosion_velocity * car.max_vel:
                            car.delete_self()
                            break  


                        car.x, car.y = car.prev_x, car.prev_y
                        car.vel *= 0.5

                elif isinstance(obj, Track):
                    if car.sprite.get_rect(topleft=(car.x, car.y)).colliderect(obj.sprite.get_rect(topleft=(obj.x, obj.y))):
                        try:
                            expected_sequence = race_progress[0][car]
                            if obj.sequence_number == expected_sequence + 1:
                                race_progress[0][car] = obj.sequence_number
                        except:
                            pass
                elif isinstance(obj, FinishLine):
                    if car.sprite.get_rect(topleft=(car.x, car.y)).colliderect(obj.sprite.get_rect(topleft=(obj.x, obj.y))):
                        try:
                            current_progress = race_progress[0][car]
                            if current_progress == race_lenght:
                                return False
                        except:
                            pass