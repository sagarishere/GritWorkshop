import neat
import random
from Game import Game
from AI_AGENT import AI_AGENT

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
        self.game_data = []
    
    def get_new_genome(self):
        # Get a new genome for a new AI agen
        
        return self.population.population[random.choice(list(self.population.population.keys()))]
    
    def run(self, generations):
        # Run for the specified number of generations
        for generation in range(generations):
            # Evaluate the current generation's genomes
            self.population.run(self.evaluate_genomes, 1)  # Run for 1 generation

            # After all agents in this generation have been evaluated, reset the game state
            self.game.reset_game_state()
        self.print_statistics()
    
    def print_statistics(self):
        # Print best genome from the latest generation
        best_genome = self.stats_reporter.best_genome()
        print(f"Best genome - ID: {best_genome.key}, Fitness: {best_genome.fitness}")
        
        # Print species count
        species_stats = self.stats_reporter.get_species_sizes()
        print(f"Species counts: {species_stats}")

    def evaluate_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            agent = AI_AGENT(genome, config)
            game_result = self.game.run(agent)
            genome.fitness = game_result['fitness']

    def set_game(self, game):
        self.game = game
#neat_core = NEATCore("path_to_config_file/config-feedforward.txt")
#neat_core.run(100)  # e.g., for 100 generations