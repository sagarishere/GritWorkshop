class TargetFunction:
    def __init__(self):
        # You can add any initialization code here if required.
        pass
        self.agent_compound_reward = {}

    def compute_fitness(self, game_data, genome_id):

        fitness = 0
        race_progress = game_data.get('race_progress', 0)
        race_length = game_data.get('race_length', 1)  # avoid division by zero



        if race_progress >= race_length:
            fitness +=1000 # maximum reward for finishing the race
        else:
            progress_ratio = race_progress / race_length
            fitness = 1000 * progress_ratio 
        


        #This needs to stay
        return fitness + self.agent_compound_reward[genome_id]

    def add_runtime_fitness(self, car_data):
        x = car_data["x"]
        y = car_data["y"]
        angle = car_data["angle"]
        vel = car_data["vel"]
        max_vel = car_data["max_vel"]
        agent = car_data["agent"]
        collision_status = car_data["collision"]

        normalized_vel = vel / max_vel
        speed_reward = normalized_vel * 0.05

        if collision_status == 1:  # Wall collision
            speed_reward -= 50
        elif collision_status == -1:  # Explosion
            speed_reward -= 100

        total_reward = speed_reward

        # Keep the existing code
        if agent not in self.agent_compound_reward:
            self.agent_compound_reward[agent.genome_id] = 0
        self.agent_compound_reward[agent.genome_id] += total_reward