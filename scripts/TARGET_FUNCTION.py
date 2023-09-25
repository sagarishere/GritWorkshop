class TargetFunction:
    def __init__(self):
        self.agent_compound_reward = {}

    def compute_fitness(self, game_data, genome_id):
        fitness = 0
        race_progress = game_data.get('race_progress', 0)
        race_length = game_data.get('race_length', 1)  # avoid division by zero


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
        elapsed_time = car_data["elapsed_time"]
        raycast_hits = car_data["raycast_hits"] #This is an array, going from left to right (I think :) )

        reward = 0



        # Keep the existing code
        if agent not in self.agent_compound_reward:
            self.agent_compound_reward[agent.genome_id] = 0
        self.agent_compound_reward[agent.genome_id] += reward