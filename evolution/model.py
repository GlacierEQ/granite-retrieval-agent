from dataclasses import dataclass
from typing import List, Dict, Any, Callable
import random
import uuid

@dataclass
class Individual:
    """Represents a single individual in the population with a specific genotype."""
    id: str
    genotype: Dict[str, Any]
    fitness: float = 0.0
    
    @classmethod
    def create_random(cls, gene_space: Dict[str, Any]):
        """Create an individual with random genes from the given gene space."""
        genotype = {}
        for gene_name, gene_range in gene_space.items():
            if isinstance(gene_range, list):
                genotype[gene_name] = random.choice(gene_range)
            elif isinstance(gene_range, tuple) and len(gene_range) == 2:
                if isinstance(gene_range[0], int) and isinstance(gene_range[1], int):
                    genotype[gene_name] = random.randint(gene_range[0], gene_range[1])
                else:
                    genotype[gene_name] = random.uniform(gene_range[0], gene_range[1])
        return cls(id=str(uuid.uuid4()), genotype=genotype)

@dataclass
class Population:
    """Collection of individuals forming a population."""
    individuals: List[Individual]
    
    def get_best(self) -> Individual:
        """Get the individual with highest fitness."""
        return max(self.individuals, key=lambda ind: ind.fitness)
    
    def get_worst(self) -> Individual:
        """Get the individual with lowest fitness."""
        return min(self.individuals, key=lambda ind: ind.fitness)
    
    def get_average_fitness(self) -> float:
        """Calculate the average fitness of the population."""
        if not self.individuals:
            return 0.0
        return sum(ind.fitness for ind in self.individuals) / len(self.individuals)
