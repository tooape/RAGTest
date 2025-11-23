"""GPU Manager for Multi-GPU Support

This module provides utilities for managing multiple GPUs and distributing
workloads across them.
"""

import logging
from typing import Optional, List
from contextlib import contextmanager
import threading

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


logger = logging.getLogger(__name__)


class GPUManager:
    """Manages GPU allocation and assignment for parallel workloads."""

    def __init__(self):
        """Initialize GPU manager and detect available GPUs."""
        self.available_gpus = []
        self.gpu_lock = threading.Lock()
        self.gpu_assignments = {}
        self._detect_gpus()

    def _detect_gpus(self):
        """Detect available GPUs using PyTorch and FAISS."""
        if TORCH_AVAILABLE and torch.cuda.is_available():
            self.available_gpus = list(range(torch.cuda.device_count()))
            logger.info(f"Detected {len(self.available_gpus)} GPUs:")
            for gpu_id in self.available_gpus:
                gpu_name = torch.cuda.get_device_name(gpu_id)
                gpu_memory = torch.cuda.get_device_properties(gpu_id).total_memory / 1e9
                logger.info(f"  GPU {gpu_id}: {gpu_name} ({gpu_memory:.1f} GB)")
        else:
            logger.warning("No GPUs detected or PyTorch not available. Using CPU mode.")

    def get_num_gpus(self) -> int:
        """Return the number of available GPUs."""
        return len(self.available_gpus)

    def has_gpus(self) -> bool:
        """Check if any GPUs are available."""
        return len(self.available_gpus) > 0

    def assign_gpu(self, task_id: str, preferred_gpu: Optional[int] = None) -> Optional[int]:
        """Assign a GPU to a task.

        Args:
            task_id: Unique identifier for the task
            preferred_gpu: Specific GPU to use (if available)

        Returns:
            GPU ID assigned to the task, or None if using CPU
        """
        if not self.has_gpus():
            return None

        with self.gpu_lock:
            # If preferred GPU is specified and available, use it
            if preferred_gpu is not None and preferred_gpu in self.available_gpus:
                self.gpu_assignments[task_id] = preferred_gpu
                return preferred_gpu

            # Otherwise, use round-robin assignment
            if task_id in self.gpu_assignments:
                return self.gpu_assignments[task_id]

            # Assign GPU with fewest current assignments
            gpu_counts = {gpu_id: 0 for gpu_id in self.available_gpus}
            for assigned_gpu in self.gpu_assignments.values():
                if assigned_gpu in gpu_counts:
                    gpu_counts[assigned_gpu] += 1

            assigned_gpu = min(gpu_counts.items(), key=lambda x: x[1])[0]
            self.gpu_assignments[task_id] = assigned_gpu

            logger.debug(f"Assigned GPU {assigned_gpu} to task '{task_id}'")
            return assigned_gpu

    def release_gpu(self, task_id: str):
        """Release GPU assignment for a task.

        Args:
            task_id: Unique identifier for the task
        """
        with self.gpu_lock:
            if task_id in self.gpu_assignments:
                gpu_id = self.gpu_assignments.pop(task_id)
                logger.debug(f"Released GPU {gpu_id} from task '{task_id}'")

    def get_device(self, task_id: str, preferred_gpu: Optional[int] = None) -> str:
        """Get PyTorch device string for a task.

        Args:
            task_id: Unique identifier for the task
            preferred_gpu: Specific GPU to use (if available)

        Returns:
            Device string ('cuda:X' or 'cpu')
        """
        gpu_id = self.assign_gpu(task_id, preferred_gpu)
        if gpu_id is not None:
            return f"cuda:{gpu_id}"
        return "cpu"

    @contextmanager
    def get_gpu_context(self, task_id: str, preferred_gpu: Optional[int] = None):
        """Context manager for GPU allocation.

        Args:
            task_id: Unique identifier for the task
            preferred_gpu: Specific GPU to use (if available)

        Yields:
            GPU ID assigned to the task, or None if using CPU
        """
        gpu_id = self.assign_gpu(task_id, preferred_gpu)
        try:
            yield gpu_id
        finally:
            self.release_gpu(task_id)

    def get_faiss_gpu_resources(self, gpu_id: int):
        """Get FAISS GPU resources for a specific GPU.

        Args:
            gpu_id: GPU ID to use

        Returns:
            FAISS GPU resources object, or None if FAISS not available
        """
        if not FAISS_AVAILABLE or not self.has_gpus():
            return None

        if faiss.get_num_gpus() == 0:
            logger.warning("FAISS GPU support not available")
            return None

        try:
            # Create GPU resources for the specific GPU
            res = faiss.StandardGpuResources()
            return res
        except Exception as e:
            logger.error(f"Failed to create FAISS GPU resources for GPU {gpu_id}: {e}")
            return None

    def get_gpu_stats(self) -> dict:
        """Get current GPU statistics.

        Returns:
            Dictionary with GPU usage information
        """
        stats = {
            "num_gpus": len(self.available_gpus),
            "gpu_ids": self.available_gpus,
            "assignments": dict(self.gpu_assignments),
        }

        if TORCH_AVAILABLE and self.has_gpus():
            gpu_info = []
            for gpu_id in self.available_gpus:
                info = {
                    "id": gpu_id,
                    "name": torch.cuda.get_device_name(gpu_id),
                    "memory_total_gb": torch.cuda.get_device_properties(gpu_id).total_memory / 1e9,
                }

                # Get memory usage if available
                try:
                    memory_allocated = torch.cuda.memory_allocated(gpu_id) / 1e9
                    memory_reserved = torch.cuda.memory_reserved(gpu_id) / 1e9
                    info["memory_allocated_gb"] = memory_allocated
                    info["memory_reserved_gb"] = memory_reserved
                except Exception:
                    pass

                gpu_info.append(info)

            stats["gpu_info"] = gpu_info

        return stats

    def clear_cache(self):
        """Clear GPU cache for all GPUs."""
        if TORCH_AVAILABLE and self.has_gpus():
            for gpu_id in self.available_gpus:
                try:
                    with torch.cuda.device(gpu_id):
                        torch.cuda.empty_cache()
                    logger.debug(f"Cleared cache for GPU {gpu_id}")
                except Exception as e:
                    logger.warning(f"Failed to clear cache for GPU {gpu_id}: {e}")


# Global GPU manager instance
_gpu_manager = None


def get_gpu_manager() -> GPUManager:
    """Get the global GPU manager instance.

    Returns:
        Global GPUManager instance
    """
    global _gpu_manager
    if _gpu_manager is None:
        _gpu_manager = GPUManager()
    return _gpu_manager


def reset_gpu_manager():
    """Reset the global GPU manager instance."""
    global _gpu_manager
    _gpu_manager = None
