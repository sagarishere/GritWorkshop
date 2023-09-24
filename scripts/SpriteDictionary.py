        
 

from Sprite import Sprite
def load_dicionary():
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

    sprite_dictionary = {
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
    return sprite_dictionary