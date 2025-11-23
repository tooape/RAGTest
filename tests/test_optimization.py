"""Tests for hyperparameter optimization."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from optimization.grid_search import GridSearchOptimizer, coarse_grid, create_grid


def test_create_grid_basic():
    """Test basic grid creation."""
    param_space = {
        "a": [1, 2],
        "b": [3, 4],
    }

    grid = create_grid(param_space)

    # Should have 2 * 2 = 4 combinations
    assert len(grid) == 4

    # Check all combinations present
    expected = [
        {"a": 1, "b": 3},
        {"a": 1, "b": 4},
        {"a": 2, "b": 3},
        {"a": 2, "b": 4},
    ]

    for combo in expected:
        assert combo in grid


def test_create_grid_single_param():
    """Test grid with single parameter."""
    param_space = {"a": [1, 2, 3]}

    grid = create_grid(param_space)

    assert len(grid) == 3
    assert grid == [{"a": 1}, {"a": 2}, {"a": 3}]


def test_create_grid_empty():
    """Test grid with empty param space."""
    grid = create_grid({})

    assert len(grid) == 1
    assert grid == [{}]


def test_coarse_grid_continuous():
    """Test coarse grid for continuous parameters."""
    param_ranges = {
        "weight": (0.0, 1.0, "continuous"),
    }

    space = coarse_grid(param_ranges)

    # Should test 5 points: min, 25%, 50%, 75%, max
    assert len(space["weight"]) == 5
    assert 0.0 in space["weight"]
    assert 1.0 in space["weight"]
    assert 0.5 in space["weight"]


def test_coarse_grid_discrete():
    """Test coarse grid for discrete parameters."""
    param_ranges = {
        "k": (10, 100, "discrete"),
    }

    space = coarse_grid(param_ranges)

    # Should test 3 points: min, mid, max
    assert len(space["k"]) == 3
    assert 10 in space["k"]
    assert 100 in space["k"]
    assert 55 in space["k"]  # (10 + 100) // 2


def test_coarse_grid_categorical():
    """Test coarse grid for categorical parameters."""
    param_ranges = {
        "method": (["min-max", "z-score", "rank"], "categorical"),
    }

    space = coarse_grid(param_ranges)

    # Should include all categories
    assert space["method"] == ["min-max", "z-score", "rank"]


def test_grid_search_optimizer():
    """Test GridSearchOptimizer basic functionality."""
    param_space = {
        "a": [1, 2],
        "b": [3, 4],
    }

    optimizer = GridSearchOptimizer(param_space)

    # Test iteration
    configs = list(optimizer)
    assert len(configs) == 4

    # Test reporting
    for i, params in enumerate(configs):
        score = i * 0.1  # Fake scores
        optimizer.report(params, score)

    # Best should be last one with highest score
    best = optimizer.get_best()
    assert best["score"] == 0.3


def test_grid_search_early_stopping():
    """Test early stopping in grid search."""
    param_space = {
        "a": list(range(10)),  # 10 values
    }

    optimizer = GridSearchOptimizer(
        param_space,
        early_stopping=True,
        patience=3,
    )

    # Report decreasing scores
    count = 0
    for params in optimizer:
        score = 1.0 - count * 0.1  # Decreasing
        optimizer.report(params, score)

        count += 1

        if optimizer.should_stop():
            break

    # Should stop after patience trials without improvement
    assert count <= 4  # 1 initial best + 3 patience


def test_grid_search_get_results_sorted():
    """Test getting sorted results."""
    param_space = {"a": [1, 2, 3]}

    optimizer = GridSearchOptimizer(param_space)

    # Report in random order
    optimizer.report({"a": 2}, 0.5)
    optimizer.report({"a": 1}, 0.8)
    optimizer.report({"a": 3}, 0.3)

    results = optimizer.get_results_sorted()

    # Should be sorted by score descending
    assert results[0]["score"] == 0.8
    assert results[1]["score"] == 0.5
    assert results[2]["score"] == 0.3


def test_grid_search_with_metadata():
    """Test storing metadata with results."""
    param_space = {"a": [1, 2]}

    optimizer = GridSearchOptimizer(param_space)

    optimizer.report(
        {"a": 1},
        0.5,
        metadata={"time": 1.5, "notes": "test"},
    )

    results = optimizer.get_results_sorted()
    assert results[0]["metadata"]["time"] == 1.5
    assert results[0]["metadata"]["notes"] == "test"


@pytest.mark.parametrize(
    "param_space,expected_size",
    [
        ({"a": [1, 2]}, 2),
        ({"a": [1, 2], "b": [3, 4]}, 4),
        ({"a": [1, 2], "b": [3, 4], "c": [5, 6]}, 8),
    ],
)
def test_grid_sizes(param_space, expected_size):
    """Test grid size calculation."""
    grid = create_grid(param_space)
    assert len(grid) == expected_size
