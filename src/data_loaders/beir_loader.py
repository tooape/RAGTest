"""BEIR dataset loader."""

import json
import os
from pathlib import Path
from typing import Dict, Optional

from loguru import logger

from .base import Dataset, Document, Query


class BEIRDataset(Dataset):
    """Loader for BEIR benchmark datasets."""

    def __init__(
        self,
        name: str,
        data_dir: str = "beir_datasets",
        split: str = "test",
    ):
        """Initialize BEIR dataset loader.

        Args:
            name: Dataset name (e.g., 'nq')
            data_dir: Directory containing BEIR datasets
            split: Dataset split to load (default: 'test')
        """
        super().__init__(name)
        self.data_dir = Path(data_dir)
        self.split = split
        self.dataset_path = self.data_dir / name

    def load(self) -> None:
        """Load BEIR dataset from disk."""
        logger.info(f"Loading BEIR dataset: {self.name} ({self.split} split)")

        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found at {self.dataset_path}. "
                f"Run download_beir.py first."
            )

        # Load corpus
        corpus_file = self.dataset_path / "corpus.jsonl"
        self._corpus = self._load_corpus(corpus_file)
        logger.info(f"Loaded {len(self._corpus):,} documents")

        # Load queries
        queries_file = self.dataset_path / "queries.jsonl"
        self._queries = self._load_queries(queries_file)
        logger.info(f"Loaded {len(self._queries):,} queries")

        # Load qrels
        qrels_file = self.dataset_path / "qrels" / f"{self.split}.tsv"
        self._qrels = self._load_qrels(qrels_file)
        logger.info(f"Loaded qrels for {len(self._qrels):,} queries")

    def _load_corpus(self, filepath: Path) -> Dict[str, Document]:
        """Load corpus from JSONL file."""
        corpus = {}
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                doc_dict = json.loads(line)
                doc_id = doc_dict["_id"]

                # Combine title and text
                title = doc_dict.get("title", "")
                text = doc_dict.get("text", "")
                combined_text = f"{title} {text}".strip() if title else text

                corpus[doc_id] = Document(
                    id=doc_id,
                    text=combined_text,
                    metadata={"title": title} if title else None,
                )
        return corpus

    def _load_queries(self, filepath: Path) -> Dict[str, Query]:
        """Load queries from JSONL file."""
        queries = {}
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                query_dict = json.loads(line)
                query_id = query_dict["_id"]
                queries[query_id] = Query(
                    id=query_id,
                    text=query_dict["text"],
                )
        return queries

    def _load_qrels(self, filepath: Path) -> Dict[str, Dict[str, int]]:
        """Load relevance judgments from TSV file.

        Format: query-id\tcorpus-id\tscore
        """
        qrels = {}
        with open(filepath, "r", encoding="utf-8") as f:
            next(f)  # Skip header
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) != 3:
                    continue

                query_id, doc_id, score = parts
                score = int(score)

                if query_id not in qrels:
                    qrels[query_id] = {}
                qrels[query_id][doc_id] = score

        return qrels


def load_beir_dataset(name: str, data_dir: str = "beir_datasets") -> BEIRDataset:
    """Convenience function to load and return a BEIR dataset.

    Args:
        name: Dataset name (e.g., 'nq')
        data_dir: Directory containing BEIR datasets

    Returns:
        Loaded BEIRDataset instance
    """
    dataset = BEIRDataset(name=name, data_dir=data_dir)
    dataset.load()
    return dataset
