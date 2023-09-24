import neat
import random

class NEATCore:
    def __init__(self, config_path):
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  config_path)
        self.population = neat.Population(self.config)
        
        # Reporters
        self.stdout_reporter = neat.StdOutReporter(True)
        self.population.add_reporter(self.stdout_reporter)
        
        self.stats_reporter = neat.StatisticsReporter()
        self.population.add_reporter(self.stats_reporter)
        
        # Checkpointer
        self.checkpointer = neat.Checkpointer(5)  # Save every 5 generations, adjust as needed
        self.population.add_reporter(self.checkpointer)
    
    def get_new_genome(self):
        # Get a new genome for a new AI agen
        
        return self.population.population[random.choice(list(self.population.population.keys()))]
    
    def run(self, fitness_function, generations):
        # Run NEAT evolution
        self.population.run(fitness_function, generations)
        
        # After running, print some statistics for debugging
        self.print_statistics()
    
    def print_statistics(self):
        # Print best genome from the latest generation
        best_genome = self.stats_reporter.best_genome()
        print(f"Best genome - ID: {best_genome.key}, Fitness: {best_genome.fitness}")
        
        # Print species count
        species_counts = self.stdout_reporter.species_count_evolution
        print(f"Species count: {species_counts[-1]}")  # Last entry
        
        # You can add more debug info as needed



#neat_core = NEATCore("path_to_config_file/config-feedforward.txt")
#neat_core.run(100)  # e.g., for 100 generations