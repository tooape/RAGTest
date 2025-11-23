"""
Tests for dependency installation and imports.

This module tests:
1. All required dependencies can be imported
2. Dependency versions meet requirements
3. Optional dependencies are handled gracefully
4. Module imports work correctly
"""

import sys
import importlib
from pathlib import Path

import pytest


class TestCoreDependencies:
    """Test that core dependencies are installed and importable."""

    def test_numpy_import(self):
        """Test that numpy is installed and importable."""
        import numpy as np

        assert hasattr(np, '__version__')
        # Verify basic functionality
        arr = np.array([1, 2, 3])
        assert arr.sum() == 6

    def test_pandas_import(self):
        """Test that pandas is installed and importable."""
        import pandas as pd

        assert hasattr(pd, '__version__')
        # Verify basic functionality
        df = pd.DataFrame({'a': [1, 2, 3]})
        assert len(df) == 3

    def test_torch_import(self):
        """Test that PyTorch is installed and importable."""
        import torch

        assert hasattr(torch, '__version__')
        # Verify basic functionality
        tensor = torch.tensor([1, 2, 3])
        assert tensor.sum().item() == 6

    def test_sentence_transformers_import(self):
        """Test that sentence-transformers is installed."""
        from sentence_transformers import SentenceTransformer

        assert SentenceTransformer is not None

    def test_faiss_import(self):
        """Test that FAISS is installed (CPU or GPU version)."""
        try:
            import faiss
            assert hasattr(faiss, 'IndexFlatL2')
        except ImportError:
            pytest.skip("FAISS not installed")

    def test_rank_bm25_import(self):
        """Test that rank-bm25 is installed."""
        from rank_bm25 import BM25Okapi

        assert BM25Okapi is not None

    def test_loguru_import(self):
        """Test that loguru is installed."""
        from loguru import logger

        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'error')

    def test_optuna_import(self):
        """Test that optuna is installed."""
        import optuna

        assert hasattr(optuna, '__version__')
        assert hasattr(optuna, 'create_study')

    def test_pytest_import(self):
        """Test that pytest is installed."""
        import pytest

        assert hasattr(pytest, '__version__')


class TestOptionalDependencies:
    """Test handling of optional dependencies."""

    def test_faiss_gpu_availability(self):
        """Test whether FAISS GPU is available."""
        try:
            import faiss

            # Check if GPU is available
            if hasattr(faiss, 'get_num_gpus'):
                num_gpus = faiss.get_num_gpus()
                # Just verify the function works, GPU may or may not be present
                assert isinstance(num_gpus, int)
        except ImportError:
            pytest.skip("FAISS not installed")

    def test_cuda_availability(self):
        """Test whether CUDA is available for PyTorch."""
        import torch

        # This should not fail even if CUDA is not available
        cuda_available = torch.cuda.is_available()
        assert isinstance(cuda_available, bool)

        if cuda_available:
            device_count = torch.cuda.device_count()
            assert device_count > 0

    def test_beir_import(self):
        """Test that BEIR is available (optional dataset loading)."""
        try:
            import beir
            assert beir is not None
        except ImportError:
            pytest.skip("BEIR not installed")


class TestModuleImports:
    """Test that all custom modules can be imported."""

    def test_import_datasets_module(self):
        """Test importing datasets module."""
        from src.datasets import Dataset, Document, Query, QRel

        assert Dataset is not None
        assert Document is not None
        assert Query is not None
        assert QRel is not None

    def test_import_beir_loader(self):
        """Test importing BEIR loader."""
        from src.datasets.beir_loader import BEIRDataset, load_beir_dataset

        assert BEIRDataset is not None
        assert load_beir_dataset is not None

    def test_import_vault_loader(self):
        """Test importing Vault loader."""
        from src.datasets.vault_loader import VaultDataset, load_vault_dataset

        assert VaultDataset is not None
        assert load_vault_dataset is not None

    def test_import_models_module(self):
        """Test importing models module."""
        from src.models import Embedder, BM25Searcher, Reranker

        assert Embedder is not None
        assert BM25Searcher is not None
        assert Reranker is not None

    def test_import_embedders(self):
        """Test importing embedders."""
        from src.models.embedders import SentenceTransformerEmbedder

        assert SentenceTransformerEmbedder is not None

    def test_import_rerankers(self):
        """Test importing rerankers."""
        from src.models.rerankers import CrossEncoderReranker

        assert CrossEncoderReranker is not None

    def test_import_bm25(self):
        """Test importing BM25."""
        from src.models.bm25 import BM25Searcher

        assert BM25Searcher is not None

    def test_import_strategies_module(self):
        """Test importing strategies module."""
        from src.strategies import (
            RetrievalStrategy,
            SemanticSearch,
            BM25Strategy,
            WeightedHybrid,
            RRFHybrid,
            MultiSignalFusion,
            TwoStageReranking,
            MultiSignalWithReranking,
            DynamicChunkingMultiSignal
        )

        assert RetrievalStrategy is not None
        assert SemanticSearch is not None
        assert BM25Strategy is not None
        assert WeightedHybrid is not None
        assert RRFHybrid is not None
        assert MultiSignalFusion is not None
        assert TwoStageReranking is not None
        assert MultiSignalWithReranking is not None
        assert DynamicChunkingMultiSignal is not None

    def test_import_evaluation_module(self):
        """Test importing evaluation module."""
        from src.evaluation.metrics import (
            mean_reciprocal_rank,
            ndcg_at_k,
            recall_at_k,
            precision_at_k
        )

        assert mean_reciprocal_rank is not None
        assert ndcg_at_k is not None
        assert recall_at_k is not None
        assert precision_at_k is not None

    def test_import_optimization_module(self):
        """Test importing optimization module."""
        from src.optimization import GridSearchOptimizer, BayesianOptimizer

        assert GridSearchOptimizer is not None
        assert BayesianOptimizer is not None

    def test_import_utils_module(self):
        """Test importing utils module."""
        from src.utils import ResultsTracker
        from src.utils.chunker import SlidingWindowChunker, SentenceAwareChunker
        from src.utils.gpu_manager import get_gpu_manager
        from src.utils.parallel_executor import StrategyExecutor

        assert ResultsTracker is not None
        assert SlidingWindowChunker is not None
        assert SentenceAwareChunker is not None
        assert get_gpu_manager is not None
        assert StrategyExecutor is not None


class TestDependencyVersions:
    """Test that dependency versions meet minimum requirements."""

    def test_numpy_version(self):
        """Test numpy version meets requirements."""
        import numpy as np
        from packaging import version

        try:
            assert version.parse(np.__version__) >= version.parse("1.24.0")
        except ImportError:
            # packaging not available, skip version check
            pytest.skip("packaging not installed for version checking")

    def test_torch_version(self):
        """Test PyTorch version meets requirements."""
        import torch
        from packaging import version

        try:
            assert version.parse(torch.__version__.split('+')[0]) >= version.parse("2.0.0")
        except ImportError:
            pytest.skip("packaging not installed for version checking")

    def test_pytest_version(self):
        """Test pytest version meets requirements."""
        import pytest
        from packaging import version

        try:
            assert version.parse(pytest.__version__) >= version.parse("7.4.0")
        except ImportError:
            pytest.skip("packaging not installed for version checking")


class TestImportPerformance:
    """Test that imports don't have circular dependencies or take too long."""

    def test_no_circular_imports(self):
        """Test that there are no circular import issues."""
        # Try importing all main modules
        try:
            from src import datasets, models, strategies, evaluation, optimization, utils
            assert True
        except ImportError as e:
            pytest.fail(f"Circular import detected: {e}")

    def test_import_strategies_performance(self):
        """Test that importing strategies module is reasonably fast."""
        import time

        start = time.time()
        # Force reimport
        if 'src.strategies' in sys.modules:
            del sys.modules['src.strategies']
        from src import strategies
        end = time.time()

        # Import should complete in less than 5 seconds
        assert (end - start) < 5.0, "Strategy module import took too long"

    def test_import_models_performance(self):
        """Test that importing models module is reasonably fast."""
        import time

        start = time.time()
        # Force reimport
        if 'src.models' in sys.modules:
            del sys.modules['src.models']
        from src import models
        end = time.time()

        # Import should complete in less than 5 seconds
        assert (end - start) < 5.0, "Models module import took too long"


class TestRequirementsTxtExists:
    """Test that requirements.txt exists and is valid."""

    def test_requirements_file_exists(self):
        """Test that requirements.txt exists."""
        requirements_path = Path(__file__).parent.parent / "requirements.txt"
        assert requirements_path.exists(), "requirements.txt not found"

    def test_requirements_file_not_empty(self):
        """Test that requirements.txt is not empty."""
        requirements_path = Path(__file__).parent.parent / "requirements.txt"
        content = requirements_path.read_text()

        # Should have some content
        assert len(content) > 0

        # Should have some package names (not just comments)
        lines = [line.strip() for line in content.split('\n')
                 if line.strip() and not line.strip().startswith('#')]
        assert len(lines) > 0

    def test_requirements_includes_core_packages(self):
        """Test that requirements.txt includes core packages."""
        requirements_path = Path(__file__).parent.parent / "requirements.txt"
        content = requirements_path.read_text()

        # Check for core packages
        assert 'numpy' in content
        assert 'torch' in content
        assert 'sentence-transformers' in content
        assert 'loguru' in content
        assert 'pytest' in content
        assert 'optuna' in content
        assert 'rank-bm25' in content


class TestSystemRequirements:
    """Test system requirements and environment."""

    def test_python_version(self):
        """Test that Python version is 3.8 or higher."""
        assert sys.version_info >= (3, 8), "Python 3.8 or higher required"

    def test_system_encoding(self):
        """Test that system encoding is UTF-8."""
        import locale

        # Get system encoding
        encoding = sys.getdefaultencoding()

        # Should support UTF-8
        assert 'utf' in encoding.lower()

    def test_import_path_includes_src(self):
        """Test that src directory is in Python path."""
        src_path = Path(__file__).parent.parent / "src"

        # Should be able to import from src
        try:
            from src import datasets
            assert True
        except ImportError:
            pytest.fail("Cannot import from src directory")
