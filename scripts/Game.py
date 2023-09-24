import pygame
from pygame.locals import *
from Renderer import Renderer
from Sprite import Sprite
from Car import Car
from Track import Track
from FinishLine import FinishLine
from Wall import Wall
from GameObject import GameObject
from MapHandler import MapHandler
from AI_AGENT import AI_AGENT
from Button import Button
from SpatialGrid import SpatialGrid
import CollisionManager
import SpriteDictionary
from TemporaryObj import TemporaryObj
from NEATCore import NEATCore

class Game:

    def __init__(self):
        # Setting up the renderer
        width = 1536
        height = 768
        self.renderer = Renderer(width, height)
        self.clock = pygame.time.Clock()
        map_handler =  MapHandler()
        self.sprite_dictionary= SpriteDictionary.load_dicionary()
        self.spatial_grid = SpatialGrid(1536, 768, 96) #96x96 256x256 384x384 192x192
        self.neat_core = NEATCore("D:\GritWorkshop\scripts\config-feedforward.txt")


        self.static_gameobjects =   []
        self.dynamic_gameobjects =  []
        self.race_progress =        [] 
        self.objects_to_remove =    []
        self.AI_AGENTS =            []

        self.TICK_RATE =         30
        self.race_lenght =       -1
        self.render_skip_count = 10
        self.current_skip =       0
        self.game_state =   "NORMAL"
        self.running =          True
        self.timer =              0  
        num_ai_cars =             50 


        self.generation = 0
        track_map = MapHandler.map_two()
        self.static_gameobjects.extend(map_handler.generate_track(track_map, 96, sprite_dictionary=self.sprite_dictionary))
        map_handler.generate_track_sequence(track_map["map_layout"], self.static_gameobjects)
        self.race_lenght = map_handler.race_lenght

        for obj in self.static_gameobjects:
            self.spatial_grid.insert(obj)
        self.finish_line = self.get_finish_line()
        self.register_gameobject(self.finish_line)
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
            if len(self.dynamic_gameobjects) == 0:
                self.game_over()

            #self.check_stop_condition()

            if self.timer > 30:
                self.reset_game_state()

            for x in range(len(self.dynamic_gameobjects)):
                if isinstance(self.dynamic_gameobjects[x], Car) and hasattr(self.dynamic_gameobjects[x], 'ai_agent'):
                    obj = self.dynamic_gameobjects[x]
                    # Set inputs for the agent
                    obj.ai_agent.AI_INPUT([obj.x, obj.y, obj.angle, obj.vel])
                self.dynamic_gameobjects[x].update()

            self.cleanup_destroyed_objects()
            formatted_timer  = '%.3f'%(self.timer)

            self.timer_text.update_text("Timer: " + str(formatted_timer ), self.renderer.width, self.renderer.height)

            if self.game_state == "SIMULATE":
                self.current_skip += 1
                if self.current_skip >= self.render_skip_count:
                    self.render_game(current_fps)
                    self.current_skip = 0 
            else:
                self.render_game(current_fps)

            if CollisionManager.check_collisions(self.dynamic_gameobjects, self.spatial_grid, self.race_progress, self.race_lenght) == False:
                self.game_over()

            self.clock.tick(self.TICK_RATE)

    def check_stop_condition(self):
        # Check progress and assign rewards
        total_cars = len(self.AI_AGENTS)  # Assuming you have a list of AI agents
        cars_that_progressed = sum(1 for progress in self.race_progress for _, value in progress.items() if value > 0)

        # If less than 10% of cars have increased their race_progress in the last 5 seconds
        if self.timer >= 5.0 and cars_that_progressed < total_cars * 0.1:
            print("RESETING DUE TO NO PROGRESS")
            self.reset_game_state()

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
            ai_car = Car(self.finish_line.x, self.finish_line.y, car_sprite, max_vel=20, rotation_vel=5, angle=270, car_explosion_velocity=0.00001 ,AI_CONTROLLED=True)

            genome = self.neat_core.get_new_genome()
            agent = AI_AGENT(genome, self.neat_core.config)
            self.AI_AGENTS.append(agent)
            ai_car.set_ai_agent_controller(agent)

            self.register_gameobject(ai_car)
            self.dynamic_gameobjects.append(ai_car)
            self.race_progress.append({ai_car: 0})  # starting from sequence 0 for each car

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
            

    def reset_game_state(self):        
        self.timer = 0
        for x in range(len(self.dynamic_gameobjects)):
            if x >= len(self.dynamic_gameobjects):
                break
            car = self.dynamic_gameobjects[x]
            # Here, we're assuming there's a method to destroy or deregister cars. 
            # You might need to adapt this to your actual method of destroying game objects.
            self.remove_gameobject(car)
            #self.deregister_gameobject(car)
        self.dynamic_gameobjects.clear()

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
        #self.game_state = "NORMAL"
        
        # Clean up any other leftover states or attributes
        self.objects_to_remove.clear()
        self.current_skip = 0
        print("Game state reset complete, generation:", self.generation)
        self.generation += 1


        


if __name__ == "__main__":
    print("starting game")
    game = Game()
    game.run()
    pygame.quit()
    print("ending game")