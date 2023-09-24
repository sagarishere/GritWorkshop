import math
from Car import Car
class RaycastManager:
    def __init__(self, spatial_grid):
        self.spatial_grid = spatial_grid
        self.max_ray_distance = 200
    
    def cast_rays_for_cars(self, game_objects):
        distances = []
        ray_positions = []

        for obj in game_objects:
            if isinstance(obj, Car):  # only cast rays for Cars
                start_pos = (obj.x, obj.y)
                direction_angle = obj.angle
                
                # Convert angle to direction vector
                dx = math.cos(math.radians(direction_angle))
                dy = math.sin(math.radians(direction_angle))
                
                distance = self.cast_ray(start_pos, (dx, dy), self.max_ray_distance)
            
                # Calculate the end position of the ray based on the distance
                end_x = obj.x + dx * distance
                end_y = obj.y + dy * distance
                ray_positions.append((start_pos, (end_x, end_y)))

        return distances, ray_positions

    def cast_ray(self, start_pos, direction, max_distance):
        """ 
        This is the cast_ray function we've discussed before. 
        It uses the spatial grid for optimized raycasting.
        """
        x, y = start_pos
        dx, dy = direction
        
        for _ in range(0, self.max_ray_distance, 50):  # Using step size of 1 for simplicity
            x += dx
            y += dy
            ray_pos = (x, y)

            nearby_walls = self.spatial_grid.get_neighboring_objects(x, y)

            for wall in nearby_walls:
                if wall.get_rect().collidepoint(ray_pos):  # Use the new method here
                    # Compute distance from start_pos to collision point
                    distance = ((x - start_pos[0])**2 + (y - start_pos[1])**2)**0.5
                    return distance

        return max_distance