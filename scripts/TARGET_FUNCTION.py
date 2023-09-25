def compute_fitness(game_data, agent_compound_reward, agent):
    race_progress = game_data.get('race_progress', 0)
    race_length = game_data.get('race_length', 1)  # avoid division by zero
    
    if race_progress >= race_length:
        fitness = 100.0  # maximum reward for finishing the race
    else:
        # compute a reward proportional to the agent's progress
        progress_ratio = race_progress / race_length
        fitness = 100.0 * progress_ratio * 5  # scaled to be out of 10

    # Add the real-time computed fitness
    fitness += agent_compound_reward.get(agent, 0)

    return fitness

def add_runtime_fitness(agent_data, agent_compound_reward):
    # Assuming agent_data looks something like:
    # {'speed': value, 'position': value, 'collision': boolean, 'rotation': value}
    
    speed_reward = agent_data.get('speed', 0) * 0.1  # weight the speed
    position_reward = agent_data.get('position', 0) * 0.2  # weight the position
    collision_penalty = -20 if agent_data.get('collision', False) else 0  # penalize for collision
    rotation_reward = agent_data.get('rotation', 0) * 0.05  # weight the rotation

    # Compound the rewards and penalties
    total_reward = speed_reward + position_reward + collision_penalty + rotation_reward

    # Update the agent_compound_reward dictionary with the new total_reward
    agent_compound_reward[agent_data['agent']] = agent_compound_reward.get(agent_data['agent'], 0) + total_reward