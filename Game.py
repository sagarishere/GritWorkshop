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


class Game:
    def __init__(self):
        # Setting up the renderer
        width = 1536
        height = 768
        self.renderer = Renderer(width, height)
        self.clock = pygame.time.Clock()
        self.running = True

        self.TICK_RATE = 30
        self.race_lenght = -1
        self.static_gameobjects = []
        self.dynamic_gameobjects = []
        self.car_indices = []

        self.car_explosion_velocity = 0.05 # This is a percentage value

        track_map = MapArchive.map_one()
        self.static_gameobjects.extend(self.generate_track(track_map, 96))
        self.generate_track_sequence(track_map, self.static_gameobjects)

        # Finish line addition
        self.finish_line = self.get_finish_line()
        self.register_gameobject(self.finish_line)

        self.test_sprite = Sprite("assets/track2.jpg")
        car1_sprite = Sprite("assets/car1.png")
        self.car1 = Car(self.finish_line.x, self.finish_line.y, car1_sprite, max_vel=20, rotation_vel=5, angle=270)
        self.register_gameobject(self.car1)
    
        self.dynamic_gameobjects.append(self.car1)
        self.car_indices.append(len(self.dynamic_gameobjects) - 1)
        self.race_progress = [{self.car1: 0}]  # starting from sequence 0 for the car
        self.timer = 0  # timer in seconds


        self.race_progress_text = self.renderer.TextObject(font_size=24, font_color=(255, 255, 0), pos=(50, 50))
        self.timer_text = self.renderer.TextObject(font_size=24, font_color=(255, 255, 0), pos=(50, 75))

        self.renderer.text_objects.extend([self.race_progress_text, self.timer_text])

        print("Init done..")


        #Todo: Add walls and track and finishline to some static arry, and have active gameobjeccts in another

    def run(self):
        while self.running:
            self.timer += 1 / self.TICK_RATE
            self.handle_events()
            self.update()
            self.renderer.RenderAllObjects(self.static_gameobjects + self.dynamic_gameobjects)
            self.renderer.RenderAllTextObjects()
            self.check_collisions()
            self.clock.tick(self.TICK_RATE)  # Limit to 30 FPS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):

        if len(self.car_indices) == 0:
            self.game_over()

        for x in range(len(self.dynamic_gameobjects)):
            self.dynamic_gameobjects[x].update()

        # for idx in self.car_indices:
        #     car = self.dynamic_gameobjects[idx]
        #     car.update()
        
        time = '%.3f'%(self.timer)
        try:
            car1 = self.dynamic_gameobjects[self.car_indices[0]]
            self.race_progress_text.update_text("Race Progress:" + str(self.race_progress[0][car1]), self.renderer.width, self.renderer.height)
            self.timer_text.update_text("Timer: " + str(time), self.renderer.width, self.renderer.height)
        except:
            pass

    def game_over(self):
        print("Game Over! Total time taken:", self.timer, "seconds")
        pass
    
    def get_finish_line(self):
        # This function should now loop over static_gameobjects
        for obj in self.static_gameobjects:
            if isinstance(obj, FinishLine):
                return obj
        return None

    def generate_track(self,track_map, map_spacing):
        game_objects = []
        track_sequence = 0  # to keep the count of track segments

        # iterate through the rows and columns of the track_map
        for y, row in enumerate(track_map):
            for x, item in enumerate(row):
                # Assuming you have sprite paths or objects defined elsewhere. 
                # Replace these with the appropriate sprites for each type.
                wall_sprite = Sprite("assets/wall.jpg")
                track_sprite = Sprite("assets/track.jpg")
                finish_line_sprite = Sprite("assets/finish.jpg")

                # Create corresponding game objects based on item's type
                if item == 0:
                    game_objects.append(FinishLine(x* map_spacing, y* map_spacing, finish_line_sprite))
                elif item == 1:
                    game_objects.append(Track(x * map_spacing, y* map_spacing, track_sprite, -1, x,y))
                    track_sequence += 1  # increment the sequence counter for the next track segment
                elif item == 2:
                    game_objects.append(Wall(x* map_spacing, y* map_spacing, wall_sprite))

        return game_objects
    
    def check_collisions(self):
        # Change this to handle dynamic objects colliding with static objects
        for idx in self.car_indices:
            car = self.dynamic_gameobjects[idx]

            for obj in self.static_gameobjects:
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
                                obj.sprite = self.test_sprite
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
        obj = TemporaryObj(x, y, explosion_sprite, 1)
        self.dynamic_gameobjects.append(obj)
        self.register_gameobject(obj)


if __name__ == "__main__":
    print("starting game")
    game = Game()
    game.run()
    pygame.quit()
    print("ending game")