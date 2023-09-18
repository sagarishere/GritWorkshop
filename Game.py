import pygame
from pygame.locals import *
import Renderer
from Sprite import Sprite
from Car import Car
from Track import Track
from FinishLine import FinishLine
from Wall import Wall
from GameObject import GameObject

import MapArchive

class Game:

    def __init__(self):
        # Setting up the renderer
        width = 1536
        height = 768
        self.renderer = Renderer.Renderer(width, height)
        self.clock = pygame.time.Clock()
        self.running = True


        self.TICK_RATE = 30
        self.race_lenght = -1
        # Create an array of active game objects
        self.active_gameobjects = []

        track_map = MapArchive.map_one()
        self.active_gameobjects.extend(self.generate_track(track_map,96))
        self.generate_track_sequence(track_map, self.active_gameobjects)

        self.finish_line = self.get_finish_line()


        # Creating game objects with sprites

        self.test_sprite = Sprite("assets/track2.jpg")

        car1_sprite = Sprite("assets/car1.png")
        self.car1 = Car(self.finish_line.x  , self.finish_line.y, car1_sprite, max_vel=20, rotation_vel=5, angle=270)
    
        self.active_gameobjects.append(self.car1)
        self.race_progress = [{self.car1: 0}]  # starting from sequence 0 for the car
        self.timer = 0  # timer in seconds

        print("Init done..")

    def run(self):

        self.timer += 1 / self.TICK_RATE
        while self.running:
            self.handle_events()

            self.update()
            self.renderer.RenderAllObjects(self.active_gameobjects)
            self.check_collisions()
            self.clock.tick(self.TICK_RATE)  # Limit to 30 FPS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):


        #Add a check for the win condtion
        for game_object in self.active_gameobjects:
            if type(game_object) == Car:
                game_object.update()
                
        
    def game_over(self):
        print("Game Over! Total time taken:", self.timer, "seconds")
        pass
    

    def get_finish_line(self):
        for obj in self.active_gameobjects:
            if isinstance(obj, FinishLine):  # Assuming you have a FinishLine class for the finish line segment
                return obj
        return None  # Return None if no FinishLine object is found


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
        car = self.car1
        for obj in self.active_gameobjects:
            if isinstance(obj, Wall):  # Assuming you have a Wall class for wall segments
                if car.sprite.get_rect(topleft=(car.x, car.y)).colliderect(obj.sprite.get_rect(topleft=(obj.x, obj.y))):
                    car.x, car.y = car.prev_x, car.prev_y
                    car.vel *= 0.5  # Slow the car's velocity by half

                # Check for collisions with track segments
            elif isinstance(obj, Track):  # Assuming you have a Track class for track segments
                if car.sprite.get_rect(topleft=(car.x, car.y)).colliderect(obj.sprite.get_rect(topleft=(obj.x, obj.y))):

                    expected_sequence = self.race_progress[0][car]  # Retrieve the last sequence number the car collided with
                    if obj.sequence_number == expected_sequence + 1:
                        self.race_progress[0][car] = obj.sequence_number  # Update the race_progress
                        obj.sprite = self.test_sprite
                 

            elif isinstance(obj, FinishLine):  # Assuming you have a Track class for track segments
                if car.sprite.get_rect(topleft=(car.x, car.y)).colliderect(obj.sprite.get_rect(topleft=(obj.x, obj.y))):

                    current_progress = self.race_progress[0][car]  # Retrieve the last sequence number the car collided with
                    if current_progress == self.race_lenght:
                        self.game_over()


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


if __name__ == "__main__":
    print("starting game")
    game = Game()
    game.run()
    pygame.quit()
    print("ending game")