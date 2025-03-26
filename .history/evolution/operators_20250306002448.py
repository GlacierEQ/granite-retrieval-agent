import random
from typing import List, Dict, Any, Tuple
import copy
from .model import Individual, Population

def select_tournament(population: Population, tournament_size: int = 3) -> Individual:
    """Select an individual using tournament selection."""
    tournament = random.sample(population.individuals, tournament_size)
    return max(tournament, key=lambda ind: ind.fitness)

def select_roulette(population: Population) -> Individual:
    """Select an individual using roulette wheel selection."""
    total_fitness = sum(max(0.01, ind.fitness) for ind in population.individuals)
    pick = random.uniform(0, total_fitness)
    current = 0
    for ind in population.individuals:
        current += max(0.01, ind.fitness)
        if current > pick:
            return ind
    return population.individuals[-1]  # Fallback

def crossover_uniform(parent1: Individual, parent2: Individual, gene_space: Dict[str, Any]) -> Tuple[Individual, Individual]:
    """Create two offspring using uniform crossover."""
    child1_genotype = {}
    child2_genotype = {}
    
    for gene in parent1.genotype:
        if random.random() < 0.5:
            child1_genotype[gene] = parent1.genotype[gene]
            child2_genotype[gene] = parent2.genotype[gene]
        else:
            child1_genotype[gene] = parent2.genotype[gene]
            child2_genotype[gene] = parent1.genotype[gene]
    
    child1 = Individual(id=str(random.getrandbits(64)), genotype=child1_genotype)
    child2 = Individual(id=str(random.getrandbits(64)), genotype=child2_genotype)
    
    return child1, child2

def mutate(individual: Individual, gene_space: Dict[str, Any], mutation_rate: float = 0.1) -> Individual:
    """Mutate an individual's genes according to the mutation rate."""
    mutated = copy.deepcopy(individual)
    
    for gene_name, value in mutated.genotype.items():
        if random.random() < mutation_rate:
            gene_range = gene_space[gene_name]
            if isinstance(gene_range, list):
                mutated.genotype[gene_name] = random.choice(gene_range)
            elif isinstance(gene_range, tuple) and len(gene_range) == 2:
                if isinstance(gene_range[0], int) and isinstance(gene_range[1], int):
                    mutated.genotype[gene_name] = random.randint(gene_range[0], gene_range[1])
                else:
                    mutated.genotype[gene_name] = random.uniform(gene_range[0], gene_range[1])
    
    return mutated
