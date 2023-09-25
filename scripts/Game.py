import pygame
from pygame.locals import *
from Renderer import Renderer
from Sprite import Sprite
from Car import Car
from FinishLine import FinishLine
from MapHandler import MapHandler
from Button import Button
from SpatialGrid import SpatialGrid
import CollisionManager
import SpriteDictionary
from Line import Line
from RaycastManager import RaycastManager
import time
import TARGET_FUNCTION
class Game:

    def __init__(self, neat_core):
        self.neat_core = neat_core
        # Setting up the renderer
        self.width = 1536
        self.height = 768
        self.renderer = Renderer(self.width, self.height)
        self.clock = pygame.time.Clock()
        map_handler =  MapHandler()
        self.sprite_dictionary= SpriteDictionary.load_dicionary()
        self.spatial_grid = SpatialGrid(1536, 768, 48) #96x96 256x256 384x384 192x192
        self.raycast_manager = RaycastManager(self.spatial_grid)

        self.static_gameobjects =   []
        self.dynamic_gameobjects =  []
        self.race_progress =        {} 
        self.objects_to_remove =    []
        self.AI_AGENTS =            []
        self.line_objects =         []
        self.all_agents =           []
        self.car_ray_angles = [0, 45, -45, 90, -90]
        self.car_max_velocity = 20
        self.TICK_RATE =         30
        self.race_lenght =       -1
        self.render_skip_count = 10
        self.current_skip =       0
        self.game_state =   "NORMAL"
        self.running =          True 
        self.timer =              0  
        self.num_ai_cars =        20


        self.generation = 0
        track_map = MapHandler.map_two()
        self.static_gameobjects.extend(map_handler.generate_track(track_map, 96, sprite_dictionary=self.sprite_dictionary))
        map_handler.generate_track_sequence(track_map["map_layout"], self.static_gameobjects)
        self.race_lenght = map_handler.race_lenght

        for obj in self.static_gameobjects:
            self.spatial_grid.insert(obj)
        self.finish_line = self.get_finish_line()
        self.register_gameobject(self.finish_line)
        #self.spawn_ai_cars(self.num_ai_cars)
        self.race_progress_text = self.renderer.TextObject(font_size=24, font_color=(255, 255, 0), pos=(50, 50))
        self.timer_text = self.renderer.TextObject(font_size=24, font_color=(255, 255, 0), pos=(50, 75))
        self.renderer.text_objects.extend([self.race_progress_text, self.timer_text])
        self.fps_text = self.renderer.TextObject(font_size=24, font_color=(255, 255, 0), pos=(50, 100))
        self.renderer.text_objects.extend([self.fps_text])
        self.simulate_button = Button(100, 10, 100, 40, "SIMULATE", self.simulate)
        self.normal_button = Button(220, 10, 100, 40, "NORMAL", self.normal)
        self.buttons = [self.simulate_button, self.normal_button]

        print("Init done..")

    def run(self, agents, target_function):
        NORMAL_TICKS_PER_SECOND = 30 
        self.reset_game_state(agents)
        while self.running:
            current_fps = self.clock.get_fps()
            logical_ticks = current_fps / NORMAL_TICKS_PER_SECOND
            elapsed_time = logical_ticks / max(NORMAL_TICKS_PER_SECOND, 1)  
            self.timer += elapsed_time
            self.handle_events()
            if len(self.dynamic_gameobjects) == 0:
                self.game_over()
                self.running = False

        
            if self.timer > 30 or self.check_stop_condition() == True:
                return self.collect_game_data()

            car_distances, ray_data = self.raycast_manager.cast_rays_for_cars(self.dynamic_gameobjects, self.car_ray_angles, self.width, self.height)

            for x in range(len(self.line_objects)):
                self.line_objects[x].SetLine(ray_data[x][0], ray_data[x][1]) 

            ray_angle_count = len(self.car_ray_angles)

            for x in range(len(self.dynamic_gameobjects)):
                obj = self.dynamic_gameobjects[x]
                if isinstance(obj, Car) and hasattr(obj, 'ai_agent'):
                    obj = obj
                    
                    start_idx = x * ray_angle_count
                    end_idx = start_idx + ray_angle_count
                    
                    car_specific_distances = car_distances[start_idx:end_idx]
                    #car_specific_distances = self.normalize(car_specific_distances)
                    normalized_x = obj.x / self.width
                    normalized_y = obj.y / self.height
                    normalized_angle = obj.angle / 360  # assuming angle is in degrees
                    normalized_vel = obj.vel / self.car_max_velocity

                    normalized_inputs = [normalized_x, normalized_y, normalized_angle, normalized_vel] + car_specific_distances
                    inputs = normalized_inputs
                    obj.ai_agent.AI_INPUT(inputs)
                
                obj.update()
                

            self.cleanup_destroyed_objects()
            formatted_timer  = '%.3f'%(self.timer)

            self.timer_text.update_text("Timer: " + str(formatted_timer ), self.renderer.width, self.renderer.height)


            collision_data = CollisionManager.check_collisions(self.dynamic_gameobjects, self.spatial_grid, self.race_progress, self.race_lenght)
            for x in range(len(self.dynamic_gameobjects)):
                obj = self.dynamic_gameobjects[x]
                if isinstance(obj, Car) and hasattr(obj, 'ai_agent'):
                    collision_status = collision_data.get(obj, 0)  # Default to 0 (no collision)

                    car_data = {
                        "x": obj.x,
                        "y": obj.y,
                        "angle": obj.angle,
                        "vel": obj.vel,
                        "max_vel": obj.max_vel,
                        "agent": obj.ai_agent,
                        "collision": collision_status,
                        "elapsed_time":self.timer
                    }

                    target_function.add_runtime_fitness(car_data)



            if self.game_state == "SIMULATE":
                self.current_skip += 1
                if self.current_skip >= self.render_skip_count:
                    self.render_game(current_fps)
                    self.current_skip = 0 
            else:
                self.render_game(current_fps)

            self.clock.tick(self.TICK_RATE)

        return self.collect_game_data()

    def check_stop_condition(self):
        # Track the time since the last movement was detected
        if not hasattr(self, "last_movement_time"):
            self.last_movement_time = None

        # Track the last position of each car
        if not hasattr(self, "last_car_positions"):
            self.last_car_positions = dict()

        current_time = time.time()

        # If there are no dynamic game objects left
        if not self.dynamic_gameobjects:
            return True

        significant_movement_detected = False

        # Check if any car has a velocity not close to zero or has moved significantly
        for obj in self.dynamic_gameobjects:
            if isinstance(obj, Car):
                # Check velocity
                if abs(obj.vel) > 0.5:
                    self.last_movement_time = current_time
                    self.last_car_positions[obj] = (obj.x, obj.y)  # update last known position
                    significant_movement_detected = True
                    break

                # Check movement on x and y axis
                last_position = self.last_car_positions.get(obj)
                if last_position:
                    distance_moved = ((obj.x - last_position[0]) ** 2 + (obj.y - last_position[1]) ** 2) ** 0.5
                    if distance_moved > 5:
                        self.last_movement_time = current_time
                        self.last_car_positions[obj] = (obj.x, obj.y)  # update last known position
                        significant_movement_detected = True
                        break
                else:
                    self.last_car_positions[obj] = (obj.x, obj.y)  # initialize if not present
        
        # If no significant movement has been detected for a second, trigger the stop condition
        if not significant_movement_detected and self.last_movement_time and current_time - self.last_movement_time > 1.0:
            return True

        return False




    def normalize(self, array):
        min_val = min(array)
        max_val = max(array)
        
        # Check for division by zero and handle the special case
        if max_val == min_val:
            return [0.5 for _ in array]
        
        return [(val - min_val) / (max_val - min_val) for val in array]
    def render_game(self, current_fps):
        # Calculate and display the FPS
        self.fps_text.update_text(f"FPS: {current_fps:.2f}", self.renderer.width, self.renderer.height)
        self.renderer.RenderAllObjects(self.static_gameobjects + self.dynamic_gameobjects)
        self.renderer.RenderAllTextObjects()
        self.renderer.RenderAllButtons(self.buttons)
        self.renderer.RenderAllLines(self.line_objects)

    def simulate(self):
        self.TICK_RATE = 999999
        self.game_state = "SIMULATE"

    def normal(self):
        self.TICK_RATE = 30  # or whatever your initial tick rate was
        self.game_state = "NORMAL"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.simulate_button.handle_event(event)
            self.normal_button.handle_event(event)

    def game_over(self):
        print("Game Over! Total time taken:", self.timer, "seconds")
    
    def mark_for_removal(self, game_object):
        """Mark a game object for removal."""
        if game_object not in self.objects_to_remove:
            self.objects_to_remove.append(game_object)

    def spawn_ai_cars(self, agents):
        car_sprite = Sprite("assets/car1.png")
        for agent in agents:
            ai_car = Car(self.finish_line.x + 48, self.finish_line.y + 48, car_sprite, self.car_max_velocity, rotation_vel=5, angle=270, car_explosion_velocity=0.2, AI_CONTROLLED=True)

            ai_car.set_ai_agent_controller(agent)  # Assign the agent to the car

            self.register_gameobject(ai_car)
            self.dynamic_gameobjects.append(ai_car)
            self.all_agents.append(ai_car)  # Continue to store a reference to the car in all_agents
            self.race_progress[ai_car] = 0

            for _ in range(len(self.car_ray_angles)):
                self.line_objects.append(Line(start=(0, 0), end=(300, 300), width=1))


    def get_finish_line(self):
        # This function should now loop over static_gameobjects
        for obj in self.static_gameobjects:
            if isinstance(obj, FinishLine):
                return obj
        return None

    def register_gameobject(self, gameobject):
        gameobject.register_observer(self)

    def cleanup_destroyed_objects(self):
        for obj in self.objects_to_remove:
            self.remove_gameobject(obj)
        self.objects_to_remove = []

    def remove_gameobject(self, gameobject):
        # Update this function to remove from dynamic_gameobjects
        if gameobject in self.dynamic_gameobjects:
            index = self.dynamic_gameobjects.index(gameobject)
            self.dynamic_gameobjects.remove(gameobject)

            # If the game object is a car, remove its associated ray angles
            if type(gameobject) == Car:
                # Reverse the loop to pop from the end to the beginning (to avoid index shifts)
                for _ in range(len(self.car_ray_angles)):
                    # Only pop if the index is valid
                    if index < len(self.line_objects):  
                        self.line_objects.pop(index)

    def reset_game_state(self, agents):        
        self.timer = 0
        self.all_agents.clear()
        for x in range(len(self.dynamic_gameobjects)):
            if x >= len(self.dynamic_gameobjects):
                break
            car = self.dynamic_gameobjects[x]
            self.remove_gameobject(car)

        self.dynamic_gameobjects.clear()
        self.line_objects.clear()

        self.race_progress = {}
        self.last_movement_time = time.time()
        self.race_progress_text.update_text("", self.renderer.width, self.renderer.height)
        self.timer_text.update_text("Timer: 0.000", self.renderer.width, self.renderer.height)
        self.fps_text.update_text("", self.renderer.width, self.renderer.height)
        
        self.spawn_ai_cars(agents)
        self.objects_to_remove.clear()
        self.current_skip = 0
        self.generation += 1
        self.running = True

    def collect_game_data(self):
        data = {}
        for x in range(len(self.all_agents)):
            obj = self.all_agents[x]
            if isinstance(obj, Car) and hasattr(obj, 'ai_agent'):
                genome_id = obj.ai_agent.genome_id
                data[genome_id] = {
                    'race_progress': self.race_progress.get(obj, 0),
                    'race_lenght':self.race_lenght
                }
        return data


    def QuitGame():
        pygame.quit()
        
