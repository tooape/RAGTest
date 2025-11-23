"""Parallel Executor for Running Strategies Concurrently

This module provides utilities for running multiple retrieval strategies
in parallel across multiple GPUs.
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import Dict, List, Callable, Any, Optional, Tuple
from dataclasses import dataclass
import threading

from .gpu_manager import get_gpu_manager

logger = logging.getLogger(__name__)


@dataclass
class Task:
    """Represents a task to be executed in parallel."""
    task_id: str
    func: Callable
    args: tuple = ()
    kwargs: dict = None
    gpu_id: Optional[int] = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


@dataclass
class TaskResult:
    """Result of a parallel task execution."""
    task_id: str
    result: Any
    success: bool
    error: Optional[Exception] = None
    execution_time: float = 0.0
    gpu_id: Optional[int] = None


class ParallelExecutor:
    """Executes tasks in parallel using thread or process pool."""

    def __init__(
        self,
        max_workers: Optional[int] = None,
        use_processes: bool = False,
        enable_gpu: bool = True,
    ):
        """Initialize parallel executor.

        Args:
            max_workers: Maximum number of parallel workers.
                         If None, defaults to number of GPUs (if available) or CPU count.
            use_processes: If True, use ProcessPoolExecutor instead of ThreadPoolExecutor.
                          Note: ProcessPoolExecutor has higher overhead and may not work well with GPUs.
            enable_gpu: If True, use GPU manager for GPU assignment.
        """
        self.use_processes = use_processes
        self.enable_gpu = enable_gpu
        self.gpu_manager = get_gpu_manager() if enable_gpu else None

        # Determine max workers
        if max_workers is None:
            if enable_gpu and self.gpu_manager and self.gpu_manager.has_gpus():
                max_workers = self.gpu_manager.get_num_gpus()
            else:
                import os
                max_workers = os.cpu_count() or 1

        self.max_workers = max_workers
        logger.info(f"Parallel executor initialized with {max_workers} workers "
                   f"({'processes' if use_processes else 'threads'})")

    def _execute_task(self, task: Task) -> TaskResult:
        """Execute a single task.

        Args:
            task: Task to execute

        Returns:
            TaskResult with execution results
        """
        start_time = time.time()
        gpu_id = None

        try:
            # Assign GPU if enabled
            if self.enable_gpu and self.gpu_manager and self.gpu_manager.has_gpus():
                gpu_id = self.gpu_manager.assign_gpu(task.task_id, task.gpu_id)
                if gpu_id is not None:
                    # Add GPU ID to kwargs if not already present
                    if 'gpu_id' not in task.kwargs:
                        task.kwargs['gpu_id'] = gpu_id
                    logger.debug(f"Task '{task.task_id}' using GPU {gpu_id}")

            # Execute the task
            result = task.func(*task.args, **task.kwargs)

            execution_time = time.time() - start_time
            logger.debug(f"Task '{task.task_id}' completed in {execution_time:.2f}s")

            return TaskResult(
                task_id=task.task_id,
                result=result,
                success=True,
                execution_time=execution_time,
                gpu_id=gpu_id,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Task '{task.task_id}' failed after {execution_time:.2f}s: {e}")
            return TaskResult(
                task_id=task.task_id,
                result=None,
                success=False,
                error=e,
                execution_time=execution_time,
                gpu_id=gpu_id,
            )

        finally:
            # Release GPU assignment
            if self.enable_gpu and self.gpu_manager:
                self.gpu_manager.release_gpu(task.task_id)

    def execute_parallel(
        self,
        tasks: List[Task],
        show_progress: bool = True,
    ) -> Dict[str, TaskResult]:
        """Execute tasks in parallel.

        Args:
            tasks: List of tasks to execute
            show_progress: If True, show progress updates

        Returns:
            Dictionary mapping task_id to TaskResult
        """
        if not tasks:
            logger.warning("No tasks to execute")
            return {}

        logger.info(f"Executing {len(tasks)} tasks in parallel with {self.max_workers} workers")

        results = {}
        executor_class = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor

        with executor_class(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self._execute_task, task): task
                for task in tasks
            }

            # Collect results as they complete
            completed = 0
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results[result.task_id] = result

                    completed += 1
                    if show_progress:
                        status = "✓" if result.success else "✗"
                        logger.info(f"[{completed}/{len(tasks)}] {status} {result.task_id} "
                                   f"({result.execution_time:.2f}s)")

                except Exception as e:
                    logger.error(f"Task '{task.task_id}' raised an exception: {e}")
                    results[task.task_id] = TaskResult(
                        task_id=task.task_id,
                        result=None,
                        success=False,
                        error=e,
                    )
                    completed += 1

        # Report summary
        successful = sum(1 for r in results.values() if r.success)
        failed = len(results) - successful
        total_time = sum(r.execution_time for r in results.values())
        avg_time = total_time / len(results) if results else 0

        logger.info(f"Parallel execution complete: {successful} succeeded, {failed} failed")
        logger.info(f"Total execution time: {total_time:.2f}s, Average: {avg_time:.2f}s")

        return results

    def execute_sequential(
        self,
        tasks: List[Task],
        show_progress: bool = True,
    ) -> Dict[str, TaskResult]:
        """Execute tasks sequentially (for comparison/debugging).

        Args:
            tasks: List of tasks to execute
            show_progress: If True, show progress updates

        Returns:
            Dictionary mapping task_id to TaskResult
        """
        if not tasks:
            logger.warning("No tasks to execute")
            return {}

        logger.info(f"Executing {len(tasks)} tasks sequentially")

        results = {}
        for i, task in enumerate(tasks, 1):
            result = self._execute_task(task)
            results[result.task_id] = result

            if show_progress:
                status = "✓" if result.success else "✗"
                logger.info(f"[{i}/{len(tasks)}] {status} {result.task_id} "
                           f"({result.execution_time:.2f}s)")

        # Report summary
        successful = sum(1 for r in results.values() if r.success)
        failed = len(results) - successful
        total_time = sum(r.execution_time for r in results.values())

        logger.info(f"Sequential execution complete: {successful} succeeded, {failed} failed")
        logger.info(f"Total execution time: {total_time:.2f}s")

        return results


class StrategyExecutor:
    """High-level executor for running multiple retrieval strategies in parallel."""

    def __init__(
        self,
        max_parallel: Optional[int] = None,
        enable_gpu: bool = True,
        sequential_mode: bool = False,
    ):
        """Initialize strategy executor.

        Args:
            max_parallel: Maximum number of strategies to run in parallel.
                         If None, uses number of available GPUs or CPU count.
            enable_gpu: If True, use GPU acceleration and multi-GPU support.
            sequential_mode: If True, run strategies sequentially instead of parallel.
        """
        self.executor = ParallelExecutor(
            max_workers=max_parallel,
            use_processes=False,  # Use threads for GPU workloads
            enable_gpu=enable_gpu,
        )
        self.sequential_mode = sequential_mode
        self.gpu_manager = get_gpu_manager() if enable_gpu else None

    def run_strategies(
        self,
        strategy_configs: List[Dict[str, Any]],
        experiment_runner: Callable,
        show_progress: bool = True,
    ) -> Dict[str, Any]:
        """Run multiple strategy experiments in parallel.

        Args:
            strategy_configs: List of strategy configuration dictionaries.
                             Each should have 'strategy_name' and 'params' keys.
            experiment_runner: Callable that runs a single strategy experiment.
                              Should accept (strategy_name, params, **kwargs) and return results.
            show_progress: If True, show progress updates.

        Returns:
            Dictionary mapping strategy_name to results
        """
        # Create tasks for each strategy
        tasks = []
        for i, config in enumerate(strategy_configs):
            strategy_name = config.get('strategy_name', f'strategy_{i}')
            params = config.get('params', {})
            gpu_id = config.get('gpu_id')  # Allow explicit GPU assignment

            task = Task(
                task_id=strategy_name,
                func=experiment_runner,
                kwargs={
                    'strategy_name': strategy_name,
                    'params': params,
                    **config.get('extra_kwargs', {})
                },
                gpu_id=gpu_id,
            )
            tasks.append(task)

        # Execute tasks
        if self.sequential_mode:
            logger.info("Running strategies sequentially (sequential_mode=True)")
            results = self.executor.execute_sequential(tasks, show_progress)
        else:
            logger.info(f"Running {len(tasks)} strategies in parallel")
            results = self.executor.execute_parallel(tasks, show_progress)

        # Extract successful results
        strategy_results = {}
        for task_id, result in results.items():
            if result.success:
                strategy_results[task_id] = result.result
            else:
                logger.error(f"Strategy '{task_id}' failed: {result.error}")
                strategy_results[task_id] = None

        return strategy_results

    def get_gpu_stats(self) -> Optional[dict]:
        """Get GPU statistics.

        Returns:
            GPU stats dictionary or None if GPU not enabled
        """
        if self.gpu_manager:
            return self.gpu_manager.get_gpu_stats()
        return None
