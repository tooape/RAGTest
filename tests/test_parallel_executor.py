"""
Tests for parallel executor functionality.

This module tests:
1. Task and TaskResult dataclasses
2. Parallel task execution
3. Sequential task execution
4. GPU integration with tasks
5. Error handling
6. Strategy executor
"""

import time
from unittest.mock import Mock, patch, MagicMock

import pytest

from src.utils.parallel_executor import (
    Task,
    TaskResult,
    ParallelExecutor,
    StrategyExecutor,
)


class TestTaskDataclass:
    """Test Task dataclass."""

    def test_task_creation_basic(self):
        """Test basic task creation."""
        def dummy_func():
            return "result"

        task = Task(task_id="test", func=dummy_func)

        assert task.task_id == "test"
        assert task.func == dummy_func
        assert task.args == ()
        assert task.kwargs == {}
        assert task.gpu_id is None

    def test_task_creation_with_args(self):
        """Test task creation with arguments."""
        def dummy_func(a, b):
            return a + b

        task = Task(
            task_id="test",
            func=dummy_func,
            args=(1, 2),
            kwargs={'extra': 'value'}
        )

        assert task.args == (1, 2)
        assert task.kwargs == {'extra': 'value'}

    def test_task_with_gpu_id(self):
        """Test task with specific GPU assignment."""
        def dummy_func():
            return "result"

        task = Task(task_id="test", func=dummy_func, gpu_id=1)

        assert task.gpu_id == 1


class TestTaskResultDataclass:
    """Test TaskResult dataclass."""

    def test_task_result_success(self):
        """Test successful task result."""
        result = TaskResult(
            task_id="test",
            result="success",
            success=True,
            execution_time=1.5
        )

        assert result.task_id == "test"
        assert result.result == "success"
        assert result.success is True
        assert result.error is None
        assert result.execution_time == 1.5

    def test_task_result_failure(self):
        """Test failed task result."""
        error = ValueError("Test error")
        result = TaskResult(
            task_id="test",
            result=None,
            success=False,
            error=error,
            execution_time=0.5
        )

        assert result.success is False
        assert result.error == error


class TestParallelExecutorInitialization:
    """Test ParallelExecutor initialization."""

    @patch('src.utils.parallel_executor.get_gpu_manager')
    def test_init_with_gpu(self, mock_get_gpu_manager):
        """Test initialization with GPU enabled."""
        mock_manager = Mock()
        mock_manager.has_gpus.return_value = True
        mock_manager.get_num_gpus.return_value = 2
        mock_get_gpu_manager.return_value = mock_manager

        executor = ParallelExecutor(enable_gpu=True)

        assert executor.enable_gpu is True
        assert executor.max_workers == 2

    @patch('src.utils.parallel_executor.get_gpu_manager')
    def test_init_without_gpu(self, mock_get_gpu_manager):
        """Test initialization without GPU."""
        executor = ParallelExecutor(enable_gpu=False)

        assert executor.enable_gpu is False
        assert executor.gpu_manager is None
        assert executor.max_workers > 0  # Should use CPU count

    def test_init_with_custom_workers(self):
        """Test initialization with custom number of workers."""
        executor = ParallelExecutor(max_workers=4, enable_gpu=False)

        assert executor.max_workers == 4

    def test_init_with_processes(self):
        """Test initialization with process pool."""
        executor = ParallelExecutor(use_processes=True, enable_gpu=False)

        assert executor.use_processes is True


class TestTaskExecution:
    """Test task execution."""

    def test_execute_simple_task(self):
        """Test executing a simple task."""
        def add(a, b):
            return a + b

        executor = ParallelExecutor(enable_gpu=False)
        task = Task(task_id="add", func=add, args=(2, 3))

        result = executor._execute_task(task)

        assert result.success is True
        assert result.result == 5
        assert result.error is None

    def test_execute_task_with_kwargs(self):
        """Test executing a task with keyword arguments."""
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        executor = ParallelExecutor(enable_gpu=False)
        task = Task(
            task_id="greet",
            func=greet,
            args=("World",),
            kwargs={"greeting": "Hi"}
        )

        result = executor._execute_task(task)

        assert result.success is True
        assert result.result == "Hi, World!"

    def test_execute_task_with_error(self):
        """Test executing a task that raises an error."""
        def failing_func():
            raise ValueError("Test error")

        executor = ParallelExecutor(enable_gpu=False)
        task = Task(task_id="fail", func=failing_func)

        result = executor._execute_task(task)

        assert result.success is False
        assert result.error is not None
        assert isinstance(result.error, ValueError)
        assert str(result.error) == "Test error"

    def test_execute_task_measures_time(self):
        """Test that task execution measures time."""
        def slow_func():
            time.sleep(0.1)
            return "done"

        executor = ParallelExecutor(enable_gpu=False)
        task = Task(task_id="slow", func=slow_func)

        result = executor._execute_task(task)

        assert result.success is True
        assert result.execution_time >= 0.1

    @patch('src.utils.parallel_executor.get_gpu_manager')
    def test_execute_task_with_gpu(self, mock_get_gpu_manager):
        """Test executing a task with GPU assignment."""
        mock_manager = Mock()
        mock_manager.has_gpus.return_value = True
        mock_manager.assign_gpu.return_value = 0
        mock_get_gpu_manager.return_value = mock_manager

        def gpu_func(gpu_id=None):
            return f"GPU {gpu_id}"

        executor = ParallelExecutor(enable_gpu=True)
        task = Task(task_id="gpu_task", func=gpu_func)

        result = executor._execute_task(task)

        assert result.success is True
        assert result.result == "GPU 0"
        assert result.gpu_id == 0
        mock_manager.assign_gpu.assert_called_once()
        mock_manager.release_gpu.assert_called_once()


class TestParallelExecution:
    """Test parallel execution of multiple tasks."""

    def test_execute_parallel_basic(self):
        """Test executing multiple tasks in parallel."""
        def square(x):
            return x * x

        executor = ParallelExecutor(max_workers=2, enable_gpu=False)

        tasks = [
            Task(task_id=f"square_{i}", func=square, args=(i,))
            for i in range(5)
        ]

        results = executor.execute_parallel(tasks, show_progress=False)

        assert len(results) == 5
        for i in range(5):
            task_id = f"square_{i}"
            assert results[task_id].success is True
            assert results[task_id].result == i * i

    def test_execute_parallel_empty_tasks(self):
        """Test executing with empty task list."""
        executor = ParallelExecutor(enable_gpu=False)

        results = executor.execute_parallel([], show_progress=False)

        assert results == {}

    def test_execute_parallel_with_failures(self):
        """Test parallel execution with some failing tasks."""
        def maybe_fail(x):
            if x % 2 == 0:
                raise ValueError(f"Failed on {x}")
            return x

        executor = ParallelExecutor(enable_gpu=False)

        tasks = [
            Task(task_id=f"task_{i}", func=maybe_fail, args=(i,))
            for i in range(4)
        ]

        results = executor.execute_parallel(tasks, show_progress=False)

        assert len(results) == 4
        assert results["task_0"].success is False
        assert results["task_1"].success is True
        assert results["task_2"].success is False
        assert results["task_3"].success is True

    def test_execute_parallel_concurrent_execution(self):
        """Test that tasks actually run in parallel."""
        executed_tasks = []

        def track_execution(task_id):
            executed_tasks.append((task_id, time.time()))
            time.sleep(0.1)
            return task_id

        executor = ParallelExecutor(max_workers=3, enable_gpu=False)

        tasks = [
            Task(task_id=f"task_{i}", func=track_execution, args=(f"task_{i}",))
            for i in range(3)
        ]

        start_time = time.time()
        results = executor.execute_parallel(tasks, show_progress=False)
        end_time = time.time()

        # All tasks should succeed
        assert all(r.success for r in results.values())

        # Total time should be less than sequential execution (3 * 0.1 = 0.3s)
        # With parallel execution, should be around 0.1s
        assert (end_time - start_time) < 0.25


class TestSequentialExecution:
    """Test sequential execution of tasks."""

    def test_execute_sequential_basic(self):
        """Test executing multiple tasks sequentially."""
        def square(x):
            return x * x

        executor = ParallelExecutor(enable_gpu=False)

        tasks = [
            Task(task_id=f"square_{i}", func=square, args=(i,))
            for i in range(5)
        ]

        results = executor.execute_sequential(tasks, show_progress=False)

        assert len(results) == 5
        for i in range(5):
            task_id = f"square_{i}"
            assert results[task_id].success is True
            assert results[task_id].result == i * i

    def test_execute_sequential_empty_tasks(self):
        """Test sequential execution with empty task list."""
        executor = ParallelExecutor(enable_gpu=False)

        results = executor.execute_sequential([], show_progress=False)

        assert results == {}

    def test_execute_sequential_order(self):
        """Test that tasks are executed in order."""
        execution_order = []

        def track_order(task_id):
            execution_order.append(task_id)
            return task_id

        executor = ParallelExecutor(enable_gpu=False)

        tasks = [
            Task(task_id=f"task_{i}", func=track_order, args=(f"task_{i}",))
            for i in range(5)
        ]

        executor.execute_sequential(tasks, show_progress=False)

        # Should execute in the order they were added
        assert execution_order == [f"task_{i}" for i in range(5)]


class TestStrategyExecutor:
    """Test StrategyExecutor class."""

    @patch('src.utils.parallel_executor.get_gpu_manager')
    def test_strategy_executor_init(self, mock_get_gpu_manager):
        """Test StrategyExecutor initialization."""
        mock_manager = Mock()
        mock_get_gpu_manager.return_value = mock_manager

        executor = StrategyExecutor(max_parallel=2, enable_gpu=True)

        assert executor.sequential_mode is False
        assert executor.executor is not None

    @patch('src.utils.parallel_executor.get_gpu_manager')
    def test_strategy_executor_sequential_mode(self, mock_get_gpu_manager):
        """Test StrategyExecutor in sequential mode."""
        mock_manager = Mock()
        mock_get_gpu_manager.return_value = mock_manager

        executor = StrategyExecutor(sequential_mode=True)

        assert executor.sequential_mode is True

    def test_run_strategies_basic(self):
        """Test running strategies with StrategyExecutor."""
        def mock_experiment_runner(strategy_name, params, **kwargs):
            return {"strategy": strategy_name, "result": params.get('value', 0) * 2}

        executor = StrategyExecutor(enable_gpu=False)

        strategy_configs = [
            {"strategy_name": "strategy1", "params": {"value": 5}},
            {"strategy_name": "strategy2", "params": {"value": 10}},
        ]

        results = executor.run_strategies(
            strategy_configs,
            mock_experiment_runner,
            show_progress=False
        )

        assert len(results) == 2
        assert results["strategy1"]["result"] == 10
        assert results["strategy2"]["result"] == 20

    def test_run_strategies_with_failure(self):
        """Test running strategies with some failures."""
        def mock_experiment_runner(strategy_name, params, **kwargs):
            if strategy_name == "failing_strategy":
                raise ValueError("Strategy failed")
            return {"strategy": strategy_name, "success": True}

        executor = StrategyExecutor(enable_gpu=False)

        strategy_configs = [
            {"strategy_name": "good_strategy", "params": {}},
            {"strategy_name": "failing_strategy", "params": {}},
        ]

        results = executor.run_strategies(
            strategy_configs,
            mock_experiment_runner,
            show_progress=False
        )

        assert len(results) == 2
        assert results["good_strategy"]["success"] is True
        assert results["failing_strategy"] is None

    def test_run_strategies_empty(self):
        """Test running with empty strategy list."""
        def mock_experiment_runner(strategy_name, params, **kwargs):
            return {"strategy": strategy_name}

        executor = StrategyExecutor(enable_gpu=False)

        results = executor.run_strategies(
            [],
            mock_experiment_runner,
            show_progress=False
        )

        assert results == {}

    def test_run_strategies_with_extra_kwargs(self):
        """Test running strategies with extra kwargs."""
        def mock_experiment_runner(strategy_name, params, dataset=None, **kwargs):
            return {"strategy": strategy_name, "dataset": dataset}

        executor = StrategyExecutor(enable_gpu=False)

        strategy_configs = [
            {
                "strategy_name": "strategy1",
                "params": {},
                "extra_kwargs": {"dataset": "test_dataset"}
            },
        ]

        results = executor.run_strategies(
            strategy_configs,
            mock_experiment_runner,
            show_progress=False
        )

        assert results["strategy1"]["dataset"] == "test_dataset"

    @patch('src.utils.parallel_executor.get_gpu_manager')
    def test_get_gpu_stats(self, mock_get_gpu_manager):
        """Test getting GPU stats from StrategyExecutor."""
        mock_manager = Mock()
        mock_manager.get_gpu_stats.return_value = {
            "num_gpus": 2,
            "gpu_ids": [0, 1]
        }
        mock_get_gpu_manager.return_value = mock_manager

        executor = StrategyExecutor(enable_gpu=True)

        stats = executor.get_gpu_stats()

        assert stats is not None
        assert stats["num_gpus"] == 2

    def test_get_gpu_stats_without_gpu(self):
        """Test getting GPU stats when GPU is disabled."""
        executor = StrategyExecutor(enable_gpu=False)

        stats = executor.get_gpu_stats()

        assert stats is None


class TestExecutorErrorHandling:
    """Test error handling in executor."""

    def test_task_exception_captured(self):
        """Test that exceptions in tasks are captured properly."""
        def raise_error():
            raise RuntimeError("Task error")

        executor = ParallelExecutor(enable_gpu=False)
        task = Task(task_id="error_task", func=raise_error)

        result = executor._execute_task(task)

        assert result.success is False
        assert result.error is not None
        assert isinstance(result.error, RuntimeError)

    def test_gpu_release_on_error(self):
        """Test that GPU is released even when task fails."""
        mock_manager = Mock()
        mock_manager.has_gpus.return_value = True
        mock_manager.assign_gpu.return_value = 0

        def failing_func(gpu_id=None):
            raise ValueError("Task failed")

        with patch('src.utils.parallel_executor.get_gpu_manager', return_value=mock_manager):
            executor = ParallelExecutor(enable_gpu=True)
            task = Task(task_id="fail_task", func=failing_func)

            result = executor._execute_task(task)

            assert result.success is False
            # GPU should still be released
            mock_manager.release_gpu.assert_called_once_with("fail_task")


class TestExecutorPerformance:
    """Test performance characteristics of executor."""

    def test_parallel_faster_than_sequential(self):
        """Test that parallel execution is faster than sequential."""
        def slow_task(x):
            time.sleep(0.05)
            return x

        executor = ParallelExecutor(max_workers=3, enable_gpu=False)

        tasks = [
            Task(task_id=f"task_{i}", func=slow_task, args=(i,))
            for i in range(6)
        ]

        # Sequential execution
        start_seq = time.time()
        executor.execute_sequential(tasks, show_progress=False)
        seq_time = time.time() - start_seq

        # Parallel execution
        start_par = time.time()
        executor.execute_parallel(tasks, show_progress=False)
        par_time = time.time() - start_par

        # Parallel should be significantly faster
        # 6 tasks * 0.05s = 0.3s sequential
        # With 3 workers: 2 batches * 0.05s = ~0.1s parallel
        assert par_time < seq_time * 0.8


class TestExecutorConfiguration:
    """Test executor configuration options."""

    def test_max_workers_configuration(self):
        """Test that max_workers is properly configured."""
        executor = ParallelExecutor(max_workers=5, enable_gpu=False)
        assert executor.max_workers == 5

    def test_process_vs_thread_executor(self):
        """Test that process/thread mode is configurable."""
        thread_executor = ParallelExecutor(use_processes=False, enable_gpu=False)
        process_executor = ParallelExecutor(use_processes=True, enable_gpu=False)

        assert thread_executor.use_processes is False
        assert process_executor.use_processes is True
