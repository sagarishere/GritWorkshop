import neat
import random

class NEATCore:
    def __init__(self, config_path):
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  config_path)
        self.population = neat.Population(self.config)
        
        # You can add reporters here if you wish
        self.population.add_reporter(neat.StdOutReporter(True))
        self.population.add_reporter(neat.StatisticsReporter())
    
    def get_new_genome(self):
        # Get a new genome for a new AI agent
        return self.population.population[random.choice(list(self.population.population.keys()))]
    
    def run(self, fitness_function, generations):
        # Run NEAT evolution
        self.population.run(fitness_function, generations)