def compute_fitness(game_data):
    #print("AGENT DATA" ,game_data)
  
    #AGENT DATA {'race_progress': 0, 'race_lenght': 64}
    race_progress = game_data.get('race_progress', 0)
    race_length = game_data.get('race_length', 1)  # avoid division by zero
    
    if race_progress >= race_length:
        return 100.0  # maximum reward for finishing the race
    else:
        # compute a reward proportional to the agent's progress
        progress_ratio = race_progress / race_length
        return 100.0 * progress_ratio * 5  # scaled to be out of 10

    #return 1.0


def add_runtime_fitess(agent_data):
    pass
    #this function should take agent specific data, speed, position, collision flags, rotations and add to a fitness buffer
    #this fitness buffer should then be added ontop of the compute_fitness function found here.
    