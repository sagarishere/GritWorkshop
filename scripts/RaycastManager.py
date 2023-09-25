import math
from Car import Car
from Wall import Wall

class RaycastManager:
    def __init__(self, spatial_grid):
        self.spatial_grid = spatial_grid
        self.max_ray_distance = 1000
    
    def cast_rays_for_cars(self, game_objects):
        distances = []
        ray_positions = []

        for obj in game_objects:
            if isinstance(obj, Car):  # only cast rays for Cars
                sprite_width = obj.sprite.image.get_width()
                sprite_height = obj.sprite.image.get_height()

                # Adjust start_pos to be the center of the sprite rect
                start_pos = (obj.x + sprite_width / 2, obj.y + sprite_height / 2)
                direction_angle = obj.angle + 90  # Adjust for the offset
                direction_angle %= 360  # Ensure the angle is between 0 and 360
                
                # Convert angle to direction vector
                dx = math.cos(math.radians(direction_angle))
                dy = -math.sin(math.radians(direction_angle))
                
                distance = self.cast_ray(start_pos, (dx, dy), self.max_ray_distance)
            
                # Calculate the end position of the ray based on the distance
                end_x = start_pos[0] + dx * distance
                end_y = start_pos[1] + dy * distance
                ray_positions.append((start_pos, (end_x, end_y)))

        return distances, ray_positions
    

    def cast_ray(self, start_pos, direction, max_distance):
        """ 
        This is the cast_ray function we've discussed before. 
        It uses the spatial grid for optimized raycasting.
        """
        x, y = start_pos
        dx, dy = direction
        
        step_size = 1
        num_steps = int(max_distance / step_size)

        for step in range(num_steps):
            x += dx * step_size
            y += dy * step_size
            ray_pos = (x, y)

            nearby_walls = self.spatial_grid.get_neighboring_objects(x, y)

            for wall in nearby_walls:
                if isinstance(wall, Wall) and wall.get_rect().collidepoint(ray_pos):  # Check type and then collision
                    # Compute distance from start_pos to collision point
                    distance = ((x - start_pos[0])**2 + (y - start_pos[1])**2)**0.5
                    #print(f"Collision detected with Wall at step {step}")
                    return distance

        return max_distance