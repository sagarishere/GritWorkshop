import pygame
from pygame.locals import *
from Renderer import Renderer
from Sprite import Sprite
from Car import Car
from Track import Track
from FinishLine import FinishLine
from Wall import Wall
from GameObject import GameObject
import MapArchive
import math
from TemporaryObj import TemporaryObj
from AI_AGENT import AI_AGENT
from Button import Button
from SpatialGrid import SpatialGrid
from NEATCore import NEATCore
class Game:

    def __init__(self):
        # Setting up the renderer
        width = 1536
        height = 768
        self.renderer = Renderer(width, height)
        self.clock = pygame.time.Clock()

        self.neat_core = NEATCore("scripts/config-feedforward.txt")

        self.running = True

        self.spatial_grid = SpatialGrid(1536, 768, 96) #96x96 256x256 384x384 192x192

        self.static_gameobjects = []
        self.dynamic_gameobjects = []
        self.car_indices = []
        self.race_progress = []  # starting from sequence 0 for the car
        self.objects_to_remove = []
        self.AI_AGENTS = []


        self.car_explosion_velocity = 0.50 # This is a percentage value
        self.TICK_RATE = 30
        self.race_lenght = -1
        self.render_skip_count = 10
        self.current_skip = 0
        self.game_state = "NORMAL"


        
        wall_sprite = Sprite("assets/wall.jpg")  # Represents value 2
        track_sprite = Sprite("assets/track.jpg")  # Represents value 1
        finish_line_sprite = Sprite("assets/finish.jpg")  # Represents value 0

        street_E = Sprite("assets/TopDownCityTextures/Environment_Textures/Street/streetE.png")
        street_N = Sprite("assets/TopDownCityTextures/Environment_Textures/Street/streetN.png")
        street_NE = Sprite("assets/TopDownCityTextures/Environment_Textures/Street/streetNE.png")
        street_NW = Sprite("assets/TopDownCityTextures/Environment_Textures/Street/streetNW.png")
        street_S = Sprite("assets/TopDownCityTextures/Environment_Textures/Street/streetS.png")
        street_SE = Sprite("assets/TopDownCityTextures/Environment_Textures/Street/streetSE.png")
        street_SW = Sprite("assets/TopDownCityTextures/Environment_Textures/Street/streetSW.png")
        street_W = Sprite("assets/TopDownCityTextures/Environment_Textures/Street/streetW.png")

        grass = Sprite("assets/TopDownCityTextures/Environment_Textures/Grass/grass.png")
        grass_with_stone = Sprite("assets/TopDownCityTextures/Environment_Textures/Grass/grassWithStone.png")

        self.sprite_dictionary = {
            0:finish_line_sprite,
            1:track_sprite,
            2:wall_sprite,
            3:street_E,
            4:street_N,
            5:street_NE,
            6:street_NW,
            7:street_S,
            8:street_SE,
            9:street_SW,
            10:street_W,
            11:grass,
            12:grass_with_stone
        }



        track_map = MapArchive.map_two()
        self.static_gameobjects.extend(self.generate_track(track_map, 96))
        self.generate_track_sequence(track_map["map_layout"], self.static_gameobjects)
        for obj in self.static_gameobjects:
            self.spatial_grid.insert(obj)
        # Finish line addition
        self.finish_line = self.get_finish_line()
        self.register_gameobject(self.finish_line)

        self.timer = 0  # timer in seconds

            # Generate AI controlled cars
        num_ai_cars = 50  # or any number you want
        self.spawn_ai_cars(num_ai_cars)

        self.race_progress_text = self.renderer.TextObject(font_size=24, font_color=(255, 255, 0), pos=(50, 50))
        self.timer_text = self.renderer.TextObject(font_size=24, font_color=(255, 255, 0), pos=(50, 75))
        self.renderer.text_objects.extend([self.race_progress_text, self.timer_text])
        self.fps_text = self.renderer.TextObject(font_size=24, font_color=(255, 255, 0), pos=(50, 100))
        self.renderer.text_objects.extend([self.fps_text])

        self.simulate_button = Button(100, 10, 100, 40, "SIMULATE", self.simulate)
        self.normal_button = Button(220, 10, 100, 40, "NORMAL", self.normal)
        self.buttons = [self.simulate_button, self.normal_button]

        print("Init done..")

    def run(self):
        NORMAL_TICKS_PER_SECOND = 30 
        print("Starting Run Loop...")
        while self.running:
            current_fps = self.clock.get_fps()
            logical_ticks = current_fps / NORMAL_TICKS_PER_SECOND
            elapsed_time = logical_ticks / max(NORMAL_TICKS_PER_SECOND, 1)  
            self.timer += elapsed_time
            self.handle_events()
            self.update()

            if self.game_state == "SIMULATE":
                # Only render every fifth frame in SIMULATE state
                self.current_skip += 1
                if self.current_skip >= self.render_skip_count:
                    self.render_game(current_fps)
                    self.current_skip = 0  # Reset counter
            else:
                # In other states, always render
                self.render_game(current_fps)

            self.check_collisions()
            self.clock.tick(self.TICK_RATE)


    def check_stop_condition(self):
        # Check progress and assign rewards
        total_cars = len(self.AI_AGENTS)  # Assuming you have a list of AI agents
        cars_that_progressed = sum(1 for progress in self.race_progress for _, value in progress.items() if value > 0)

        # If less than 10% of cars have increased their race_progress in the last 5 seconds
        if self.timer >= 5.0 and cars_that_progressed < total_cars * 0.1:
            # Here, you can end the episode early if needed
            print("RESETING DUE TO NO PROGRESS")
            self.reset_game_state()


    def update(self):
        if len(self.car_indices) == 0:
            self.game_over()

        self.check_stop_condition()
        for x in range(len(self.dynamic_gameobjects)):
            if isinstance(self.dynamic_gameobjects[x], Car) and hasattr(self.dynamic_gameobjects[x], 'ai_agent'):  # Assuming your car objects have an 'ai_agent' attribute
                obj = self.dynamic_gameobjects[x]
                # Set inputs for the agent
                obj.ai_agent.AI_INPUT([obj.x, obj.y, obj.angle, obj.vel])
            self.dynamic_gameobjects[x].update()

        self.cleanup_destroyed_objects()
        formatted_timer  = '%.3f'%(self.timer)

        #self.race_progress_text.update_text("Race Progress:" + str(self.race_progress[0][car1]), self.renderer.width, self.renderer.height)
        self.timer_text.update_text("Timer: " + str(formatted_timer ), self.renderer.width, self.renderer.height)

    def render_game(self, current_fps):
        # Calculate and display the FPS
        self.fps_text.update_text(f"FPS: {current_fps:.2f}", self.renderer.width, self.renderer.height)
        
        self.renderer.RenderAllObjects(self.static_gameobjects + self.dynamic_gameobjects)
        self.renderer.RenderAllTextObjects()
        self.renderer.RenderAllButtons(self.buttons)

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
        pass
    
    def mark_for_removal(self, game_object):
        """Mark a game object for removal."""
        if game_object not in self.objects_to_remove:
            self.objects_to_remove.append(game_object)

    def spawn_ai_cars(self, num_cars):
        car_sprite = Sprite("assets/car1.png")
        for _ in range(num_cars):
            ai_car = Car(self.finish_line.x, self.finish_line.y, car_sprite, max_vel=20, rotation_vel=5, angle=270, AI_CONTROLLED=True)

            genome = self.neat_core.get_new_genome()
            agent = AI_AGENT(genome, self.neat_core.config)
            self.AI_AGENTS.append(agent)
            ai_car.set_ai_agent_controller(agent)

            self.register_gameobject(ai_car)
            self.dynamic_gameobjects.append(ai_car)
            self.car_indices.append(len(self.dynamic_gameobjects) - 1)
            self.race_progress.append({ai_car: 0})  # starting from sequence 0 for each car

    def get_finish_line(self):
        # This function should now loop over static_gameobjects
        for obj in self.static_gameobjects:
            if isinstance(obj, FinishLine):
                return obj
        return None

    def generate_track(self, track_map, map_spacing):
        game_objects = []
        track_sequence = 0  # to keep the count of track segments
        track_map = MapArchive.translate_map_layout(track_map["map_layout"])
        # iterate through the rows and columns of the track_map
        for y in range(len(track_map["map_layout"])):
            for x in range(len(track_map["map_layout"][y])):

                # Assuming you have sprite paths or objects defined elsewhere.
                # Replace these with the appropriate sprites for each type.


                # Accessing the item directly using y and x indices
                item = track_map["map_layout"][y][x]
                sprite = self.sprite_dictionary[track_map["map_sprites"][y][x]]

                # Create corresponding game objects based on item's type
                if item == 0:
                    game_objects.append(FinishLine(x * map_spacing, y * map_spacing, sprite))
                elif item == 1:
                    game_objects.append(Track(x * map_spacing, y * map_spacing, sprite, -1, x, y))
                    track_sequence += 1  # increment the sequence counter for the next track segment
                elif item == 2:
                    game_objects.append(Wall(x * map_spacing, y * map_spacing, sprite))

        return game_objects
    
    def check_collisions(self):
        for idx in self.car_indices:
            car = self.dynamic_gameobjects[idx]
            neighboring_objects = self.spatial_grid.get_neighboring_objects(car.x, car.y)
            
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

                        if car.vel > self.car_explosion_velocity * car.max_vel and (angle_difference > math.radians(45)):
                            print("Car exploded!")
                            self.create_explosion(car.x, car.y)
                            self.remove_gameobject(car)
                            break  # Exit the inner loop (obj loop) and move to the next car, if any


                        car.x, car.y = car.prev_x, car.prev_y
                        car.vel *= 0.5

                elif isinstance(obj, Track):
                    if car.sprite.get_rect(topleft=(car.x, car.y)).colliderect(obj.sprite.get_rect(topleft=(obj.x, obj.y))):
                        try:
                            expected_sequence = self.race_progress[0][car]
                            if obj.sequence_number == expected_sequence + 1:
                                self.race_progress[0][car] = obj.sequence_number
                        except:
                            pass
                elif isinstance(obj, FinishLine):
                    if car.sprite.get_rect(topleft=(car.x, car.y)).colliderect(obj.sprite.get_rect(topleft=(obj.x, obj.y))):
                        try:
                            current_progress = self.race_progress[0][car]
                            if current_progress == self.race_lenght:
                                self.game_over()
                        except:
                            pass

    def generate_track_sequence(self, track_map, active_gameobjects):
        # Helper function to get the next track segment
        def get_next_segment(x, y, visited):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(track_map) and 0 <= ny < len(track_map[0]) and (nx, ny) not in visited and track_map[nx][ny] == 1:
                    return nx, ny
            return None, None

        # Recursive function to assign sequence numbers
        def dfs(x, y, sequence):
            visited.add((x, y))
            for obj in active_gameobjects:

                if isinstance(obj, Track):
                    # print("need:", x,y, " Gets:" ,obj.array_pos_x, obj.array_pos_y)
                    if obj.array_pos_x == y and obj.array_pos_y == x:
                        obj.sequence_number = sequence
                        break
            nx, ny = get_next_segment(x, y, visited)
            if nx is not None:
                dfs(nx, ny, sequence + 1)
            else:
                self.race_lenght = sequence

                print("SEQUENCE:", sequence)

        # Find the finish line
        start_x, start_y = None, None
        for i in range(len(track_map)):
            for j in range(len(track_map[i])):
                if track_map[i][j] == 0:
                    start_x, start_y = i, j
                    print("Found starting line at: " ,i,j)
                    break
            if start_x is not None:
                print("Found starting line2")
                break

        # Initialize visited set and start the DFS
        visited = {(start_x, start_y)}
        next_x, next_y = get_next_segment(start_x, start_y, visited)
        dfs(next_x, next_y, 0)

    def register_gameobject(self, gameobject):
        """Register the game as an observer for the game object."""
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
            
            if isinstance(gameobject, Car):
                if index in self.car_indices:
                    self.car_indices.remove(index)
                    for i in range(len(self.car_indices)):
                        if self.car_indices[i] > index:
                            self.car_indices[i] -= 1

    def create_explosion(self, x, y):
        # Added explosion to dynamic_gameobjects
        explosion_sprite = Sprite("assets/explosion.png")
        obj = TemporaryObj(x, y, explosion_sprite, 1, mark_for_removal_callback=self.mark_for_removal)
        self.dynamic_gameobjects.append(obj)
        self.register_gameobject(obj)

    def reset_game_state(self):        
        for idx, car in enumerate(self.car_indices):
            agent = car.ai_agent  # Assuming each car has a reference to its AI agent
            progress = self.race_progress[idx]
            reward = progress / self.race_lenght  # X being the total length or max progress value
            agent.genome.fitness = reward  # Assign the reward as fitness

        # Reset the timer
        self.timer = 0
        
        # Remove all dynamic game objects and AI cars
        for idx in self.car_indices:
            car = self.dynamic_gameobjects[idx]
            # Here, we're assuming there's a method to destroy or deregister cars. 
            # You might need to adapt this to your actual method of destroying game objects.
            self.remove_gameobject(car)
            #self.deregister_gameobject(car)
        self.dynamic_gameobjects.clear()
        self.car_indices.clear()

        # Reset race progress
        self.race_progress = []
        
        # Reset texts
        self.race_progress_text.update_text("", self.renderer.width, self.renderer.height)
        self.timer_text.update_text("Timer: 0.000", self.renderer.width, self.renderer.height)
        self.fps_text.update_text("", self.renderer.width, self.renderer.height)
        
        # Repopulate AI cars
        num_ai_cars = 50
        self.spawn_ai_cars(num_ai_cars)
        
        # Reset game state
        self.game_state = "NORMAL"
        
        # Clean up any other leftover states or attributes
        self.objects_to_remove.clear()
        self.current_skip = 0
        print("Game state reset complete.")


        


if __name__ == "__main__":
    print("starting game")
    game = Game()
    game.run()
    pygame.quit()
    print("ending game")