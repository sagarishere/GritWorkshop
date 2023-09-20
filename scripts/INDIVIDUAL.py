import random

class Individual:
    def __init__(self, genes=None):
        # Randomly initialize genes if not provided
        self.genes = genes if genes else [random.random() for _ in range(4)]  # Since there are 4 outputs for the AI_AGENT

    def crossover(self, other):
        # Simple one-point crossover
        point = random.randint(1, len(self.genes) - 1)
        child_genes = self.genes[:point] + other.genes[point:]
        return Individual(child_genes)

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.random()