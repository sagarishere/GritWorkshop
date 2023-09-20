from INDIVIDUAL import Individual
import random


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

    def run(self):
        for generation in range(self.generations):
            selected = self.selection()
            children = []
            for i in range(0, len(selected), 2):
                child1 = selected[i].crossover(selected[i+1])
                child2 = selected[i+1].crossover(selected[i])
                child1.mutate(self.mutation_rate)
                child2.mutate(self.mutation_rate)
                children.extend([child1, child2])
            self.population = children

            # Print the best individual in the current generation
            best_individual = max(self.population, key=self.fitness)
            print(f"Generation {generation + 1}: Best fitness = {self.fitness(best_individual)}")