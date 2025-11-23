"""Grid search for hyperparameter optimization."""

import itertools
from typing import Any, Dict, List

from loguru import logger


def create_grid(param_space: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    """Create grid of hyperparameter combinations.

    Args:
        param_space: Dict mapping parameter name -> list of values

    Returns:
        List of parameter dictionaries (one per combination)

    Example:
        >>> param_space = {
        ...     'semantic_weight': [0.3, 0.5, 0.7],
        ...     'bm25_weight': [0.3, 0.5],
        ... }
        >>> grid = create_grid(param_space)
        >>> len(grid)
        6
    """
    if not param_space:
        return [{}]

    # Get parameter names and values
    names = list(param_space.keys())
    value_lists = [param_space[name] for name in names]

    # Generate all combinations
    combinations = list(itertools.product(*value_lists))

    # Convert to list of dicts
    grid = [dict(zip(names, combo)) for combo in combinations]

    logger.info(f"Created grid with {len(grid)} combinations")
    return grid


def coarse_grid(param_ranges: Dict[str, tuple]) -> Dict[str, List[Any]]:
    """Create coarse grid from parameter ranges.

    Tests extremes and middle values.

    Args:
        param_ranges: Dict mapping param -> (min, max, type)
            type can be 'continuous', 'discrete', or 'categorical'

    Returns:
        Parameter space with coarse sampling

    Example:
        >>> param_ranges = {
        ...     'semantic_weight': (0.3, 0.9, 'continuous'),
        ...     'top_k': (10, 100, 'discrete'),
        ...     'normalization': (['min-max', 'z-score', 'rank'], 'categorical'),
        ... }
        >>> space = coarse_grid(param_ranges)
    """
    param_space = {}

    for name, spec in param_ranges.items():
        if len(spec) == 2:
            # Categorical
            values, _ = spec
            param_space[name] = values
        else:
            # Continuous or discrete
            min_val, max_val, param_type = spec

            if param_type == 'continuous':
                # Test: min, 25%, 50%, 75%, max
                mid = (min_val + max_val) / 2
                q1 = (min_val + mid) / 2
                q3 = (mid + max_val) / 2
                param_space[name] = [min_val, q1, mid, q3, max_val]

            elif param_type == 'discrete':
                # Test: min, middle, max
                mid = (min_val + max_val) // 2
                param_space[name] = [min_val, mid, max_val]

    return param_space


class GridSearchOptimizer:
    """Grid search hyperparameter optimizer."""

    def __init__(
        self,
        param_space: Dict[str, List[Any]],
        early_stopping: bool = False,
        patience: int = 5,
    ):
        """Initialize grid search.

        Args:
            param_space: Parameter grid
            early_stopping: Whether to stop early if no improvement
            patience: Number of trials without improvement before stopping
        """
        self.param_space = param_space
        self.grid = create_grid(param_space)
        self.early_stopping = early_stopping
        self.patience = patience

        self.results = []
        self.best_score = float('-inf')
        self.best_params = None
        self.trials_without_improvement = 0

    def __iter__(self):
        """Iterate over parameter combinations."""
        for params in self.grid:
            yield params

    def report(self, params: Dict[str, Any], score: float, metadata: Dict = None):
        """Report result for a parameter combination.

        Args:
            params: Parameters tested
            score: Score achieved
            metadata: Additional information
        """
        self.results.append({
            'params': params,
            'score': score,
            'metadata': metadata or {},
        })

        # Check for improvement
        if score > self.best_score:
            self.best_score = score
            self.best_params = params
            self.trials_without_improvement = 0
            logger.info(f"New best: {score:.4f} with {params}")
        else:
            self.trials_without_improvement += 1

    def should_stop(self) -> bool:
        """Check if early stopping criteria met."""
        if not self.early_stopping:
            return False
        return self.trials_without_improvement >= self.patience

    def get_best(self) -> Dict[str, Any]:
        """Get best parameters found."""
        return {
            'params': self.best_params,
            'score': self.best_score,
        }

    def get_results_sorted(self) -> List[Dict]:
        """Get all results sorted by score (descending)."""
        return sorted(self.results, key=lambda x: x['score'], reverse=True)
