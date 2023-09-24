

import math
from Wall import Wall
from Track import Track
from Car import Car
from FinishLine import FinishLine


def check_collisions(car_indices, dynamic_gameobjects, spatial_grid, race_progress):
        for idx in car_indices:
            car = dynamic_gameobjects[idx]
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

                        if car.vel > car.car_explosion_velocity * car.max_vel and (angle_difference > math.radians(45)):
                            print("Car exploded!")
                            car.create_explosion(car.x, car.y)
                            car.delete_self(car)
                            break  # Exit the inner loop (obj loop) and move to the next car, if any


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
                            if current_progress == self.race_lenght:
                                self.game_over()
                        except:
                            pass