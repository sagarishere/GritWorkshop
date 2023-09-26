from Track import Track
from FinishLine import FinishLine
from Wall import Wall

class MapHandler:
    def __init__(self):
        self.race_length = -1
    def map_one(): # 16x8
        # 0:finish_line_sprite, 
        # 1:track_sprite,
        # 2:wall_sprite,
        # 3:street_E,
        # 4:street_N,
        # 5:street_NE,
        # 6:street_NW,
        # 7:street_S,
        # 8:street_SE,
        # 9:street_SW,
        # 10:street_W,
        # 11:grass,
        # 12:grass_with_stone    
        return { 
            "map_layout":[ #1 = Track, 2 = WALL, 0 = start
                [1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
                [1, 2, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2],
                [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        }



    def map_two(): # 16x8
        return {
            "map_layout": [
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2],
                [2, 1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2],
                [2, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2],
                [2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2],
                [2, 1, 0, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                ]
        }


    def map_four():
        return [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 1, 2, 2, 2, 2, 1, 2],
        [2, 1, 2, 2, 2, 2, 1, 2],
        [2, 1, 2, 0, 0, 2, 1, 2],
        [2, 1, 2, 2, 2, 2, 1, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 2, 2, 2, 2, 2, 1, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 1, 2, 2, 2, 2, 2, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2]
    ]




    def map_three(): #8x8
        return [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 1, 2, 2, 2, 2, 1, 2],
        [2, 1, 2, 2, 2, 2, 1, 2],
        [2, 1, 2, 2, 2, 2, 1, 2],
        [2, 1, 2, 2, 2, 2, 1, 2],
        [2, 1, 1, 0, 1, 1, 1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2]
    ]

    race_lenght = -1
    def generate_track(self, track_map, map_spacing, sprite_dictionary):
        game_objects = []
        track_sequence = 0  # to keep the count of track segments
        track_map = self.translate_map_layout(track_map["map_layout"])
        # iterate through the rows and columns of the track_map
        for y in range(len(track_map["map_layout"])):
            for x in range(len(track_map["map_layout"][y])):

                # Assuming you have sprite paths or objects defined elsewhere.
                # Replace these with the appropriate sprites for each type.


                # Accessing the item directly using y and x indices
                item = track_map["map_layout"][y][x]
                sprite = sprite_dictionary[track_map["map_sprites"][y][x]]

                # Create corresponding game objects based on item's type
                if item == 0:
                    game_objects.append(FinishLine(x * map_spacing, y * map_spacing, sprite))
                elif item == 1:
                    game_objects.append(Track(x * map_spacing, y * map_spacing, sprite, -1, x, y))
                    track_sequence += 1  # increment the sequence counter for the next track segment
                elif item == 2:
                    game_objects.append(Wall(x * map_spacing, y * map_spacing, sprite))

        return game_objects


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
        def dfs(self,x, y, sequence):
            visited.add((x, y))
            for obj in active_gameobjects:

                if isinstance(obj, Track):
                    # print("need:", x,y, " Gets:" ,obj.array_pos_x, obj.array_pos_y)
                    if obj.array_pos_x == y and obj.array_pos_y == x:
                        obj.sequence_number = sequence
                        break
            nx, ny = get_next_segment(x, y, visited)
            if nx is not None:
                dfs(self,nx, ny, sequence + 1)
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
        dfs(self, next_x, next_y, 0)



    def translate_map_layout(self, map_layout):
        rows, cols = len(map_layout), len(map_layout[0])
        map_sprites = [[0] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                # Check surrounding tiles:
                top = map_layout[i-1][j] if i-1 >= 0 else None
                bottom = map_layout[i+1][j] if i+1 < rows else None
                left = map_layout[i][j-1] if j-1 >= 0 else None
                right = map_layout[i][j+1] if j+1 < cols else None

                # Convert the tile:
                if map_layout[i][j] == 2:  # wall
                    map_sprites[i][j] = 11 if (i + j) % 2 == 0 else 12
                elif map_layout[i][j] == 0:  # start
                    map_sprites[i][j] = 0
                else:  # track
                    if (left in [1, 0] and right in [1, 0]):
                        map_sprites[i][j] = 4  # Street N
                    elif (top in [1, 0] and bottom in [1, 0]):
                        map_sprites[i][j] = 3  # Street E
                    elif (left in [1, 0] and right in [1, 0]):
                        map_sprites[i][j] = 7  # Street S
                    elif (top in [1, 0] and bottom in [1, 0]):
                        map_sprites[i][j] = 10  # Street W
                    elif (right in [1, 0] and bottom in [1, 0]):
                        map_sprites[i][j] = 6  # Street NW
                    elif (bottom in [1, 0] and left in [1, 0]):
                        map_sprites[i][j] = 5  # Street NE
                    elif (top in [1, 0] and right in [1, 0]):
                        map_sprites[i][j] = 9  # Street SW
                    elif (top in [1, 0] and left in [1, 0]):
                        map_sprites[i][j] = 8  # Street SE
                    else:
                        map_sprites[i][j] = 1  # default track sprite

        return {
            "map_layout": map_layout,
            "map_sprites": map_sprites
        }