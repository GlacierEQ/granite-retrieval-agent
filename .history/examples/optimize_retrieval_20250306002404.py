import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evolution import EvolutionEngine, RetrievalAgentFitnessEvaluator
from typing import Dict, Any, List
import json
import matplotlib.pyplot as plt

# Mock retrieval agent for demonstration
class MockRetrievalAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        # Simulate retrieval based on config parameters
        results = []
        
        # This is just a mock implementation
        # In a real system, these parameters would affect actual retrieval
        num_results = min(10, max(1, int(self.config.get("num_results", 5))))
        threshold = self.config.get("threshold", 0.5)
        use_reranking = self.config.get("use_reranking", False)
        
        # Generate mock results
        for i in range(num_results):
            score = (1.0 - (i / num_results)) * (0.5 + threshold)
            if use_reranking:
                score *= 1.2
            
            if score < 0.2:  # Cutoff for low quality results
                break
                
            results.append({
                "id": f"doc_{i}",
                "score": score,
                "content": f"Content related to {query}"
            })
            
        return results

def agent_factory(genotype: Dict[str, Any]) -> MockRetrievalAgent:
    """Factory function to create a retrieval agent from a genotype."""
    return MockRetrievalAgent(genotype)

def main():
    # Define the gene space for our retrieval agent parameters
    gene_space = {
        "num_results": (1, 20),
        "threshold": (0.1, 0.9),
        "use_reranking": [True, False],
        "embed_dim": [64, 128, 256, 512],
        "index_type": ["flat", "hnsw", "ivf"],
        "chunk_size": (100, 1000),
    }
    
    # Mock test data
    test_queries = [
        "how to implement gradient descent",
        "comparing neural network architectures",
        "best practices for machine learning"
    ]
    
    # Mock reference results
    reference_results = [
        [{"id": f"doc_{i}", "score": 0.9 - (i * 0.05)} for i in range(5)],
        [{"id": f"doc_{i}", "score": 0.95 - (i * 0.07)} for i in range(4)],
        [{"id": f"doc_{i}", "score": 0.85 - (i * 0.04)} for i in range(6)]
    ]
    
    # Create fitness evaluator
    evaluator = RetrievalAgentFitnessEvaluator(
        test_queries=test_queries,
        reference_results=reference_results,
        agent_factory=agent_factory
    )
    
    # Create evolution engine
    evolution = EvolutionEngine(
        gene_space=gene_space,
        fitness_function=evaluator.evaluate,
        population_size=30,
        generations=20,
        mutation_rate=0.2,
        elitism=2
    )
    
    # Run evolution
    best_individual = evolution.evolve()
    
    print("\nEvolution complete!")
    print(f"Best individual: {best_individual}")
    print(f"Genotype: {best_individual.genotype}")
    print(f"Fitness: {best_individual.fitness}")
    
    # Save results
    with open("evolution_results.json", "w") as f:
        json.dump({
            "best_genotype": best_individual.genotype,
            "best_fitness": best_individual.fitness,
            "history": evolution.history
        }, f, indent=2)
    
    # Plot fitness progress
    generations = [h["generation"] for h in evolution.history]
    avg_fitness = [h["avg_fitness"] for h in evolution.history]
    best_fitness = [h["best_fitness"] for h in evolution.history]
    
    plt.figure(figsize=(10, 6))
    plt.plot(generations, avg_fitness, label="Average Fitness")
    plt.plot(generations, best_fitness, label="Best Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Evolution Progress")
    plt.legend()
    plt.grid(True)
    plt.savefig("evolution_progress.png")
    plt.show()

if __name__ == "__main__":
    main()
