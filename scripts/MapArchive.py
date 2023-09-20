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
            [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
        "map_sprites": [ 
            [6, 4, 5, 12, 11, 12, 6, 4, 5, 12, 12, 12, 12, 12, 12, 12],
            [3, 12, 9, 4, 0, 4, 8, 11, 9, 4, 4, 4, 4, 4, 4, 5],
            [3, 11, 12, 12, 11, 12, 12, 11, 12, 11, 12, 11, 11, 12, 11, 3],
            [3, 12, 6, 4, 4, 4, 4, 5, 12, 6, 4, 4, 4, 4, 4, 8],
            [3, 11, 3, 12, 12, 12, 12, 3, 12, 3, 12, 12, 11, 12, 12, 11],
            [3, 11, 9, 4, 4, 5, 11, 3, 11, 9, 4, 4, 4, 4, 4, 5],
            [3, 12, 12, 12, 12, 3, 12, 3, 12, 12, 12, 12, 12, 12, 11, 3],
            [9, 4, 4, 4, 4, 8, 11, 9, 4, 4, 4, 4, 4, 4, 4, 8]]
    }




def map_four(): # 16x8
    return [
    [1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
    [1, 2, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2],
    [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def map_two():
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