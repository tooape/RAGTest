"""
Tests for GPU manager functionality.

This module tests:
1. GPU detection and initialization
2. GPU assignment and release
3. Load balancing across multiple GPUs
4. Context manager usage
5. FAISS GPU integration
6. Thread safety
"""

import logging
import threading
from unittest.mock import Mock, patch, MagicMock

import pytest


class TestGPUManagerInitialization:
    """Test GPU manager initialization and detection."""

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_init_with_gpus(self, mock_torch):
        """Test initialization when GPUs are available."""
        # Mock CUDA availability
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 2
        mock_torch.cuda.get_device_name.side_effect = ['GPU 0', 'GPU 1']
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        assert manager.get_num_gpus() == 2
        assert manager.has_gpus() is True
        assert manager.available_gpus == [0, 1]

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_init_without_gpus(self, mock_torch):
        """Test initialization when no GPUs are available."""
        mock_torch.cuda.is_available.return_value = False

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        assert manager.get_num_gpus() == 0
        assert manager.has_gpus() is False
        assert manager.available_gpus == []

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', False)
    def test_init_without_torch(self):
        """Test initialization when PyTorch is not available."""
        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        assert manager.get_num_gpus() == 0
        assert manager.has_gpus() is False


class TestGPUAssignment:
    """Test GPU assignment functionality."""

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_assign_gpu_basic(self, mock_torch):
        """Test basic GPU assignment."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 2
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        # Assign GPU to first task
        gpu_id = manager.assign_gpu("task1")
        assert gpu_id in [0, 1]

        # Same task should get same GPU
        gpu_id2 = manager.assign_gpu("task1")
        assert gpu_id2 == gpu_id

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_assign_preferred_gpu(self, mock_torch):
        """Test assigning a preferred GPU."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 2
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        # Assign preferred GPU
        gpu_id = manager.assign_gpu("task1", preferred_gpu=1)
        assert gpu_id == 1

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_assign_gpu_load_balancing(self, mock_torch):
        """Test that GPUs are distributed evenly across tasks."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 2
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        # Assign 4 tasks
        assignments = []
        for i in range(4):
            gpu_id = manager.assign_gpu(f"task{i}")
            assignments.append(gpu_id)

        # Should distribute evenly: 2 tasks per GPU
        assert assignments.count(0) == 2
        assert assignments.count(1) == 2

    def test_assign_gpu_without_gpus(self):
        """Test GPU assignment when no GPUs are available."""
        from src.utils.gpu_manager import GPUManager

        with patch('src.utils.gpu_manager.TORCH_AVAILABLE', False):
            manager = GPUManager()

            gpu_id = manager.assign_gpu("task1")
            assert gpu_id is None


class TestGPURelease:
    """Test GPU release functionality."""

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_release_gpu(self, mock_torch):
        """Test releasing a GPU assignment."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 1
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        # Assign GPU
        gpu_id = manager.assign_gpu("task1")
        assert gpu_id == 0
        assert "task1" in manager.gpu_assignments

        # Release GPU
        manager.release_gpu("task1")
        assert "task1" not in manager.gpu_assignments

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_release_nonexistent_task(self, mock_torch):
        """Test releasing a task that was never assigned."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 1
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        # Should not raise an error
        manager.release_gpu("nonexistent_task")


class TestGPUDeviceString:
    """Test getting device strings for PyTorch."""

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_get_device_with_gpu(self, mock_torch):
        """Test getting device string when GPU is available."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 2
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        device = manager.get_device("task1")
        assert device in ["cuda:0", "cuda:1"]

    def test_get_device_without_gpu(self):
        """Test getting device string when no GPU is available."""
        from src.utils.gpu_manager import GPUManager

        with patch('src.utils.gpu_manager.TORCH_AVAILABLE', False):
            manager = GPUManager()

            device = manager.get_device("task1")
            assert device == "cpu"

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_get_device_with_preferred_gpu(self, mock_torch):
        """Test getting device string with preferred GPU."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 2
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        device = manager.get_device("task1", preferred_gpu=1)
        assert device == "cuda:1"


class TestGPUContextManager:
    """Test GPU context manager."""

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_context_manager_assigns_and_releases(self, mock_torch):
        """Test that context manager assigns and releases GPU."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 1
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        # Use context manager
        with manager.get_gpu_context("task1") as gpu_id:
            assert gpu_id == 0
            assert "task1" in manager.gpu_assignments

        # Should be released after context
        assert "task1" not in manager.gpu_assignments

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_context_manager_releases_on_exception(self, mock_torch):
        """Test that context manager releases GPU even on exception."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 1
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        # Use context manager with exception
        try:
            with manager.get_gpu_context("task1") as gpu_id:
                assert gpu_id == 0
                raise ValueError("Test exception")
        except ValueError:
            pass

        # Should still be released
        assert "task1" not in manager.gpu_assignments


class TestFAISSGPUIntegration:
    """Test FAISS GPU integration."""

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.FAISS_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    @patch('src.utils.gpu_manager.faiss')
    def test_get_faiss_gpu_resources(self, mock_faiss, mock_torch):
        """Test getting FAISS GPU resources."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 1
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)
        mock_faiss.get_num_gpus.return_value = 1
        mock_faiss.StandardGpuResources.return_value = Mock()

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        resources = manager.get_faiss_gpu_resources(0)
        assert resources is not None

    @patch('src.utils.gpu_manager.FAISS_AVAILABLE', False)
    def test_get_faiss_gpu_resources_without_faiss(self):
        """Test getting FAISS GPU resources when FAISS is not available."""
        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        resources = manager.get_faiss_gpu_resources(0)
        assert resources is None


class TestGPUStats:
    """Test GPU statistics functionality."""

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_get_gpu_stats_with_gpus(self, mock_torch):
        """Test getting GPU stats when GPUs are available."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 2
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)
        mock_torch.cuda.memory_allocated.return_value = 1e9
        mock_torch.cuda.memory_reserved.return_value = 2e9

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()
        manager.assign_gpu("task1")

        stats = manager.get_gpu_stats()

        assert stats["num_gpus"] == 2
        assert stats["gpu_ids"] == [0, 1]
        assert "task1" in stats["assignments"]
        assert "gpu_info" in stats
        assert len(stats["gpu_info"]) == 2

    def test_get_gpu_stats_without_gpus(self):
        """Test getting GPU stats when no GPUs are available."""
        from src.utils.gpu_manager import GPUManager

        with patch('src.utils.gpu_manager.TORCH_AVAILABLE', False):
            manager = GPUManager()

            stats = manager.get_gpu_stats()

            assert stats["num_gpus"] == 0
            assert stats["gpu_ids"] == []
            assert stats["assignments"] == {}


class TestGPUCacheClear:
    """Test GPU cache clearing."""

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_clear_cache(self, mock_torch):
        """Test clearing GPU cache."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 1
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)
        mock_torch.cuda.device = MagicMock()
        mock_torch.cuda.empty_cache = Mock()

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()
        manager.clear_cache()

        # Should call empty_cache for each GPU
        assert mock_torch.cuda.empty_cache.called


class TestGlobalGPUManager:
    """Test global GPU manager instance."""

    def test_get_gpu_manager_singleton(self):
        """Test that get_gpu_manager returns singleton."""
        from src.utils.gpu_manager import get_gpu_manager, reset_gpu_manager

        # Reset to ensure clean state
        reset_gpu_manager()

        # Get manager twice
        manager1 = get_gpu_manager()
        manager2 = get_gpu_manager()

        # Should be the same instance
        assert manager1 is manager2

    def test_reset_gpu_manager(self):
        """Test resetting the global GPU manager."""
        from src.utils.gpu_manager import get_gpu_manager, reset_gpu_manager

        # Get manager
        manager1 = get_gpu_manager()

        # Reset
        reset_gpu_manager()

        # Get manager again
        manager2 = get_gpu_manager()

        # Should be different instances
        assert manager1 is not manager2


class TestThreadSafety:
    """Test thread safety of GPU manager."""

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_concurrent_gpu_assignment(self, mock_torch):
        """Test that GPU assignment is thread-safe."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 2
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        # Track assignments
        assignments = []
        lock = threading.Lock()

        def assign_task(task_id):
            gpu_id = manager.assign_gpu(task_id)
            with lock:
                assignments.append((task_id, gpu_id))

        # Create multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=assign_task, args=(f"task{i}",))
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # All tasks should have assignments
        assert len(assignments) == 10

        # All GPU IDs should be valid
        for _, gpu_id in assignments:
            assert gpu_id in [0, 1]

    @patch('src.utils.gpu_manager.TORCH_AVAILABLE', True)
    @patch('src.utils.gpu_manager.torch')
    def test_concurrent_release(self, mock_torch):
        """Test that GPU release is thread-safe."""
        mock_torch.cuda.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 1
        mock_torch.cuda.get_device_name.return_value = 'Test GPU'
        mock_torch.cuda.get_device_properties.return_value = Mock(total_memory=8e9)

        from src.utils.gpu_manager import GPUManager

        manager = GPUManager()

        # Assign GPUs
        for i in range(5):
            manager.assign_gpu(f"task{i}")

        # Release from multiple threads
        def release_task(task_id):
            manager.release_gpu(task_id)

        threads = []
        for i in range(5):
            thread = threading.Thread(target=release_task, args=(f"task{i}",))
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # All assignments should be released
        assert len(manager.gpu_assignments) == 0
