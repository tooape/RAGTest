"""Bayesian optimization using Optuna."""

from typing import Any, Callable, Dict, List, Optional

import optuna
from loguru import logger
from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler


class BayesianOptimizer:
    """Bayesian hyperparameter optimizer using Optuna."""

    def __init__(
        self,
        param_space: Dict[str, tuple],
        n_trials: int = 30,
        direction: str = "maximize",
        n_startup_trials: int = 10,
        study_name: Optional[str] = None,
    ):
        """Initialize Bayesian optimizer.

        Args:
            param_space: Parameter space specification
                Format: {
                    'param_name': ('continuous', min, max),
                    'param_name': ('discrete', min, max, step),
                    'param_name': ('categorical', [val1, val2, ...]),
                }
            n_trials: Number of trials to run
            direction: 'maximize' or 'minimize'
            n_startup_trials: Random trials before Bayesian optimization
            study_name: Optional study name for persistence
        """
        self.param_space = param_space
        self.n_trials = n_trials
        self.direction = direction

        # Create Optuna study
        sampler = TPESampler(
            n_startup_trials=n_startup_trials,
            multivariate=True,
        )
        pruner = MedianPruner(n_warmup_steps=5)

        self.study = optuna.create_study(
            direction=direction,
            sampler=sampler,
            pruner=pruner,
            study_name=study_name,
        )

    def suggest_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        """Suggest parameters for a trial.

        Args:
            trial: Optuna trial object

        Returns:
            Dictionary of suggested parameters
        """
        params = {}

        for name, spec in self.param_space.items():
            param_type = spec[0]

            if param_type == 'continuous':
                _, low, high = spec
                params[name] = trial.suggest_float(name, low, high)

            elif param_type == 'discrete':
                _, low, high, step = spec
                params[name] = trial.suggest_int(name, low, high, step=step)

            elif param_type == 'categorical':
                _, choices = spec
                params[name] = trial.suggest_categorical(name, choices)

            else:
                raise ValueError(f"Unknown parameter type: {param_type}")

        return params

    def optimize(
        self,
        objective_fn: Callable[[Dict[str, Any]], float],
        show_progress: bool = True,
    ) -> Dict[str, Any]:
        """Run Bayesian optimization.

        Args:
            objective_fn: Function that takes params dict and returns score
            show_progress: Whether to show progress bar

        Returns:
            Best parameters found
        """
        def objective(trial):
            # Get suggested parameters
            params = self.suggest_params(trial)

            # Evaluate objective
            try:
                score = objective_fn(params)
                return score
            except Exception as e:
                logger.error(f"Trial failed: {e}")
                # Return worst possible score for failed trials
                return float('-inf') if self.direction == 'maximize' else float('inf')

        # Run optimization
        self.study.optimize(
            objective,
            n_trials=self.n_trials,
            show_progress_bar=show_progress,
        )

        logger.info(f"Optimization complete. Best score: {self.study.best_value:.4f}")

        return {
            'params': self.study.best_params,
            'score': self.study.best_value,
            'n_trials': len(self.study.trials),
        }

    def get_best(self) -> Dict[str, Any]:
        """Get best parameters found."""
        return {
            'params': self.study.best_params,
            'score': self.study.best_value,
        }

    def get_param_importances(self) -> Dict[str, float]:
        """Get parameter importances.

        Returns:
            Dict mapping parameter name -> importance score
        """
        try:
            return optuna.importance.get_param_importances(self.study)
        except:
            logger.warning("Could not compute parameter importances")
            return {}


def multi_objective_optimize(
    param_space: Dict[str, tuple],
    objectives: List[Callable[[Dict[str, Any]], float]],
    directions: List[str],
    n_trials: int = 30,
) -> List[Dict[str, Any]]:
    """Multi-objective Bayesian optimization.

    Args:
        param_space: Parameter space
        objectives: List of objective functions
        directions: List of directions ('maximize' or 'minimize')
        n_trials: Number of trials

    Returns:
        List of Pareto-optimal parameter sets
    """
    sampler = TPESampler(n_startup_trials=10, multivariate=True)

    study = optuna.create_study(
        directions=directions,
        sampler=sampler,
    )

    def objective(trial):
        # Get suggested parameters
        params = {}
        for name, spec in param_space.items():
            param_type = spec[0]

            if param_type == 'continuous':
                _, low, high = spec
                params[name] = trial.suggest_float(name, low, high)
            elif param_type == 'discrete':
                _, low, high, step = spec
                params[name] = trial.suggest_int(name, low, high, step=step)
            elif param_type == 'categorical':
                _, choices = spec
                params[name] = trial.suggest_categorical(name, choices)

        # Evaluate all objectives
        scores = []
        for obj_fn in objectives:
            try:
                score = obj_fn(params)
                scores.append(score)
            except Exception as e:
                logger.error(f"Objective failed: {e}")
                scores.append(float('-inf'))

        return tuple(scores)

    # Run optimization
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

    # Get Pareto-optimal trials
    pareto_trials = [
        {
            'params': trial.params,
            'scores': trial.values,
        }
        for trial in study.best_trials
    ]

    logger.info(f"Found {len(pareto_trials)} Pareto-optimal solutions")

    return pareto_trials
