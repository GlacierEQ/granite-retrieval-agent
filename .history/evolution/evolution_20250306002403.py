from typing import List, Dict, Any, Callable, Optional
import random
from .model import Individual, Population
from .operators import select_tournament, select_roulette, crossover_uniform, mutate

class EvolutionEngine:
    def __init__(
        self,
        gene_space: Dict[str, Any],
        fitness_function: Callable[[Individual], float],
        population_size: int = 50,
        generations: int = 100,
        mutation_rate: float = 0.1,
        elitism: int = 1,
        tournament_size: int = 3,
        selection_method: str = "tournament"
    ):
        self.gene_space = gene_space
        self.fitness_function = fitness_function
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.tournament_size = tournament_size
        self.selection_method = selection_method
        self.best_individual: Optional[Individual] = None
        self.history: List[Dict[str, Any]] = []
        
    def initialize_population(self) -> Population:
        """Create an initial random population."""
        individuals = [Individual.create_random(self.gene_space) for _ in range(self.population_size)]
        return Population(individuals=individuals)
    
    def evaluate_population(self, population: Population):
        """Calculate fitness for all individuals in the population."""
        for individual in population.individuals:
            individual.fitness = self.fitness_function(individual)
    
    def select_parent(self, population: Population) -> Individual:
        """Select a parent for reproduction."""
        if self.selection_method == "tournament":
            return select_tournament(population, self.tournament_size)
        else:
            return select_roulette(population)
    
    def evolve(self) -> Individual:
        """Run the evolutionary process."""
        # Initialize population
        current_population = self.initialize_population()
        self.evaluate_population(current_population)
        
        self.best_individual = current_population.get_best()
        
        for generation in range(self.generations):
            new_population = Population(individuals=[])
            
            # Elitism: Copy best individuals
            if self.elitism > 0:
                sorted_individuals = sorted(current_population.individuals, 
                                           key=lambda ind: ind.fitness, 
                                           reverse=True)
                elites = sorted_individuals[:self.elitism]
                new_population.individuals.extend(elites)
            
            # Generate offspring for the rest of the population
            while len(new_population.individuals) < self.population_size:
                # Parent selection
                parent1 = self.select_parent(current_population)
                parent2 = self.select_parent(current_population)
                
                # Crossover
                child1, child2 = crossover_uniform(parent1, parent2, self.gene_space)
                
                # Mutation
                child1 = mutate(child1, self.gene_space, self.mutation_rate)
                child2 = mutate(child2, self.gene_space, self.mutation_rate)
                
                # Add to new population
                new_population.individuals.append(child1)
                if len(new_population.individuals) < self.population_size:
                    new_population.individuals.append(child2)
            
            # Evaluate new population
            self.evaluate_population(new_population)
            
            # Update best individual
            generation_best = new_population.get_best()
            if generation_best.fitness > self.best_individual.fitness:
                self.best_individual = generation_best
            
            # Record statistics
            self.history.append({
                "generation": generation,
                "avg_fitness": new_population.get_average_fitness(),
                "best_fitness": generation_best.fitness,
                "best_genotype": generation_best.genotype
            })
            
            # Replace current population
            current_population = new_population
            
            print(f"Generation {generation}: Best Fitness = {self.best_individual.fitness}")
        
        return self.best_individual
