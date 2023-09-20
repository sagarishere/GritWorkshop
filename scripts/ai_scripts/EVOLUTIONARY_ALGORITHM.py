from INDIVIDUAL import Individual
import random
from game_scripts import Game

class EVOLUTIONARY_ALGORITHM:
    def __init__(self, agent, population_size=50, mutation_rate=0.01, generations=100):
        self.agent = agent
        self.population = [Individual() for _ in range(population_size)]
        self.mutation_rate = mutation_rate
        self.generations = generations

    def fitness(self, individual):
        # Use the individual's genes to set the AI_AGENT's decisions and get the reward/fitness
        self.agent.AI_INPUT()  # Prepare the agent if needed
        decisions = individual.genes
        reward = self.agent.TARGET_FUNCTION(decisions)  # Assumes TARGET_FUNCTION takes decisions as an input
        return reward

    def selection(self):
        # Tournament selection as an example
        selected = []
        for _ in range(len(self.population)):
            i, j = random.sample(self.population, 2)
            selected.append(i if self.fitness(i) > self.fitness(j) else j)
        return selected

    def evaluate_population(self, game):
        for individual in self.population:
            # Start the game with the current AI_AGENT's genes as the decision input
            game.reset_game_state()  # Reset the game to its initial state
            game.run(individual)  # This will run the game loop using this individual's genes


    def run(self, game):
            for generation in range(self.generations):
                # Evaluate each individual's fitness by running the game
                fitness_values = [self.evaluate_individual(game, ind) for ind in self.population]

                # Selection
                selected = self.selection(fitness_values)
                
                # Crossover and Mutation to produce the next generation
                children = []
                for i in range(0, len(selected), 2):
                    child1 = selected[i].crossover(selected[i+1])
                    child2 = selected[i+1].crossover(selected[i])
                    child1.mutate(self.mutation_rate)
                    child2.mutate(self.mutation_rate)
                    children.extend([child1, child2])

                self.population = children
                
                # Print the best individual in the current generation
                best_fitness = max(fitness_values)
                print(f"Generation {generation + 1}: Best fitness = {best_fitness}")


# Usage:
game_instance = Game()
evo_algo = EVOLUTIONARY_ALGORITHM(agent=None)  # Assuming the agent parameter is not necessary now
evo_algo.run(game_instance)