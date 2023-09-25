class TargetFunction:
    def __init__(self):
        # You can add any initialization code here if required.
        pass

    def compute_fitness(self, game_data):
        race_progress = game_data.get('race_progress', 0)
        race_length = game_data.get('race_length', 1)  # avoid division by zero

        if race_progress >= race_length:
            return 100.0  # maximum reward for finishing the race
        else:
            progress_ratio = race_progress / race_length
            return 100.0 * progress_ratio * 5  # scaled to be out of 10
        
    def add_runtime_fitness(self, x, y, angle, vel, max_vel, agent, agent_compound_reward):

        normalized_vel = vel / max_vel
        speed_reward = normalized_vel * 0.1
        total_reward =  speed_reward

        # Update the agent_compound_reward dictionary with the new total_reward
        if agent not in agent_compound_reward:
            agent_compound_reward[agent] = 0
        agent_compound_reward[agent] += total_reward