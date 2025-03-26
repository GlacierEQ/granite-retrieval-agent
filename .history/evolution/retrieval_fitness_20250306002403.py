from typing import Dict, Any, List, Callable
from .model import Individual
import random

class RetrievalAgentFitnessEvaluator:
    """Evaluates fitness of retrieval agents using test cases."""
    
    def __init__(
        self, 
        test_queries: List[str],
        reference_results: List[List[Dict[str, Any]]],
        agent_factory: Callable[[Dict[str, Any]], Any],
        metrics: Dict[str, float] = {"precision": 0.5, "recall": 0.3, "latency": 0.2}
    ):
        """
        Initialize the evaluator.
        
        Args:
            test_queries: List of test queries to evaluate
            reference_results: Expected results for each test query
            agent_factory: Function to create a retrieval agent from genotype
            metrics: Dictionary of metrics to use and their weights
        """
        self.test_queries = test_queries
        self.reference_results = reference_results
        self.agent_factory = agent_factory
        self.metrics = metrics
        
    def calculate_precision_recall(self, retrieved: List[Dict[str, Any]], reference: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate precision and recall for retrieval results."""
        retrieved_ids = set(item.get("id") for item in retrieved)
        reference_ids = set(item.get("id") for item in reference)
        
        true_positives = len(retrieved_ids.intersection(reference_ids))
        
        precision = true_positives / len(retrieved) if retrieved else 0
        recall = true_positives / len(reference) if reference else 0
        
        return {"precision": precision, "recall": recall}
    
    def evaluate(self, individual: Individual) -> float:
        """Evaluate the fitness of an individual retrieval agent."""
        agent = self.agent_factory(individual.genotype)
        
        total_score = 0.0
        
        for i, query in enumerate(self.test_queries):
            try:
                # Execute retrieval
                results = agent.retrieve(query)
                
                # Calculate metrics
                pr_metrics = self.calculate_precision_recall(results, self.reference_results[i])
                
                # Simulate latency evaluation (replace with actual measurements in real implementation)
                latency = random.uniform(0.1, 1.0) * (1.0 / (0.5 + sum(pr_metrics.values())))
                
                # Calculate weighted score
                query_score = (
                    self.metrics.get("precision", 0) * pr_metrics["precision"] +
                    self.metrics.get("recall", 0) * pr_metrics["recall"] +
                    self.metrics.get("latency", 0) * (1.0 - min(latency, 1.0))
                )
                
                total_score += query_score
                
            except Exception as e:
                print(f"Error evaluating query {query}: {e}")
                # Penalize failures
                total_score -= 1.0
                
        # Normalize by number of queries
        return total_score / len(self.test_queries) if self.test_queries else 0.0
