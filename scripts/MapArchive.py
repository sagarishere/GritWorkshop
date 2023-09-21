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
            [1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1],
            [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1],
            [1, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1],
            [1, 2, 0, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1],
            [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
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


def translate_map_layout(map_layout):
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