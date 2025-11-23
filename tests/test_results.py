"""Tests for results tracking."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import json
import tempfile

import pandas as pd
import pytest

from utils.results import ResultsTracker, load_results


def test_results_tracker_basic():
    """Test basic ResultsTracker functionality."""
    tracker = ResultsTracker()

    # Add result
    tracker.add_result(
        strategy_name="semantic",
        dataset_name="test",
        params={"weight": 0.5},
        metrics={"ndcg@10": 0.75},
    )

    assert len(tracker.results) == 1
    assert tracker.results[0]["strategy"] == "semantic"
    assert tracker.results[0]["dataset"] == "test"


def test_results_tracker_multiple_results():
    """Test adding multiple results."""
    tracker = ResultsTracker()

    for i in range(5):
        tracker.add_result(
            strategy_name=f"strategy_{i}",
            dataset_name="test",
            params={"param": i},
            metrics={"score": i * 0.1},
        )

    assert len(tracker.results) == 5


def test_results_tracker_save_json():
    """Test saving results to JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tracker = ResultsTracker(output_dir=tmpdir)

        tracker.add_result(
            strategy_name="test",
            dataset_name="test",
            params={"a": 1},
            metrics={"score": 0.5},
        )

        filepath = tracker.save_json()

        # Check file exists
        assert filepath.exists()

        # Check contents
        with open(filepath) as f:
            data = json.load(f)

        assert "results" in data
        assert len(data["results"]) == 1


def test_results_tracker_save_csv():
    """Test saving results to CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tracker = ResultsTracker(output_dir=tmpdir)

        tracker.add_result(
            strategy_name="test",
            dataset_name="test",
            params={"a": 1, "b": 2},
            metrics={"score": 0.5, "ndcg": 0.7},
            metadata={"time": 1.5},
        )

        filepath = tracker.save_csv()

        # Check file exists
        assert filepath.exists()

        # Check contents
        df = pd.read_csv(filepath)

        assert len(df) == 1
        assert "strategy" in df.columns
        assert "param_a" in df.columns
        assert "metric_score" in df.columns


def test_results_tracker_get_best():
    """Test getting best result by metric."""
    tracker = ResultsTracker()

    tracker.add_result("s1", "test", {}, {"ndcg@10": 0.5})
    tracker.add_result("s2", "test", {}, {"ndcg@10": 0.8})
    tracker.add_result("s3", "test", {}, {"ndcg@10": 0.6})

    best = tracker.get_best_by_metric("ndcg@10", dataset="test")

    assert best["strategy"] == "s2"
    assert best["metrics"]["ndcg@10"] == 0.8


def test_results_tracker_get_best_filtered():
    """Test getting best with filters."""
    tracker = ResultsTracker()

    tracker.add_result("s1", "dataset1", {}, {"score": 0.5})
    tracker.add_result("s2", "dataset1", {}, {"score": 0.8})
    tracker.add_result("s1", "dataset2", {}, {"score": 0.9})

    # Best for dataset1
    best = tracker.get_best_by_metric("score", dataset="dataset1")
    assert best["strategy"] == "s2"
    assert best["metrics"]["score"] == 0.8

    # Best for strategy s1
    best = tracker.get_best_by_metric("score", strategy="s1")
    assert best["dataset"] == "dataset2"
    assert best["metrics"]["score"] == 0.9


def test_results_tracker_summary_table():
    """Test summary table generation."""
    tracker = ResultsTracker()

    # Add multiple runs for same strategy/dataset
    tracker.add_result("s1", "d1", {"v": 1}, {"ndcg@10": 0.5, "mrr@10": 0.6})
    tracker.add_result("s1", "d1", {"v": 2}, {"ndcg@10": 0.7, "mrr@10": 0.8})
    tracker.add_result("s2", "d1", {"v": 1}, {"ndcg@10": 0.6, "mrr@10": 0.7})

    df = tracker.get_summary_table()

    # Should have 2 rows (s1-d1 and s2-d1)
    assert len(df) == 2

    # Check columns
    assert "strategy" in df.columns
    assert "dataset" in df.columns
    assert "n_runs" in df.columns

    # s1 should have 2 runs
    s1_row = df[df["strategy"] == "s1"].iloc[0]
    assert s1_row["n_runs"] == 2

    # Best NDCG for s1 should be 0.7
    assert s1_row["best_ndcg@10"] == 0.7


def test_load_results():
    """Test loading results from file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save results
        tracker1 = ResultsTracker(output_dir=tmpdir)
        tracker1.add_result("s1", "d1", {"a": 1}, {"score": 0.5})
        filepath = tracker1.save_json()

        # Load results
        tracker2 = load_results(filepath)

        assert len(tracker2.results) == 1
        assert tracker2.results[0]["strategy"] == "s1"


def test_results_tracker_metadata():
    """Test metadata storage."""
    tracker = ResultsTracker()

    tracker.add_result(
        strategy_name="test",
        dataset_name="test",
        params={},
        metrics={"score": 0.5},
        metadata={"latency_ms": 100, "notes": "test run"},
    )

    assert tracker.results[0]["metadata"]["latency_ms"] == 100
    assert tracker.results[0]["metadata"]["notes"] == "test run"
