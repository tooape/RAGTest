"""Vault dataset loader for Obsidian personal knowledge base."""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from .base import Dataset, Document, Query


class VaultDataset(Dataset):
    """Loader for Obsidian vault test dataset."""

    def __init__(
        self,
        vault_dir: str = "vault copy",
        queries_file: Optional[str] = None,
        qrels_file: Optional[str] = None,
    ):
        """Initialize Vault dataset loader.

        Args:
            vault_dir: Directory containing vault markdown files
            queries_file: Path to queries JSON file (optional, will create from test cases)
            qrels_file: Path to qrels JSON file (optional, needs to be created manually)
        """
        super().__init__("vault")
        self.vault_dir = Path(vault_dir)
        self.queries_file = Path(queries_file) if queries_file else None
        self.qrels_file = Path(qrels_file) if qrels_file else None

    def load(self) -> None:
        """Load vault dataset."""
        logger.info(f"Loading Vault dataset from {self.vault_dir}")

        if not self.vault_dir.exists():
            raise FileNotFoundError(
                f"Vault directory not found: {self.vault_dir}"
            )

        # Load corpus (all markdown files)
        self._corpus = self._load_vault_corpus()
        logger.info(f"Loaded {len(self._corpus):,} vault documents")

        # Load queries
        if self.queries_file and self.queries_file.exists():
            self._queries = self._load_queries_from_file()
        else:
            self._queries = self._create_default_queries()
        logger.info(f"Loaded {len(self._queries):,} test queries")

        # Load qrels if available
        if self.qrels_file and self.qrels_file.exists():
            self._qrels = self._load_qrels_from_file()
            logger.info(f"Loaded qrels for {len(self._qrels):,} queries")
        else:
            logger.warning(
                "No qrels file provided. Ground truth not available. "
                "Manual labeling required for evaluation."
            )
            self._qrels = {}

    def _load_vault_corpus(self) -> Dict[str, Document]:
        """Load all markdown files from vault as corpus."""
        corpus = {}

        # Walk through vault directory
        for md_file in self.vault_dir.rglob("*.md"):
            # Skip hidden files and directories
            if any(part.startswith(".") for part in md_file.parts):
                continue

            # Create document ID from relative path
            rel_path = md_file.relative_to(self.vault_dir)
            doc_id = str(rel_path)

            # Read content
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract title (first H1 heading or filename)
                title = self._extract_title(content, md_file.stem)

                # Extract metadata from frontmatter
                metadata = self._extract_frontmatter(content)
                metadata["filepath"] = str(rel_path)
                metadata["title"] = title

                # Remove frontmatter from content
                content = self._remove_frontmatter(content)

                corpus[doc_id] = Document(
                    id=doc_id,
                    text=content,
                    metadata=metadata,
                )
            except Exception as e:
                logger.warning(f"Failed to load {md_file}: {e}")
                continue

        return corpus

    def _extract_title(self, content: str, fallback: str) -> str:
        """Extract title from markdown content."""
        # Look for first H1 heading
        h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        return fallback

    def _extract_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from markdown."""
        metadata = {}
        fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if fm_match:
            # Simple key: value parsing (not full YAML)
            for line in fm_match.group(1).split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip().strip('"')
        return metadata

    def _remove_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from content."""
        return re.sub(r"^---\n.*?\n---\n", "", content, count=1, flags=re.DOTALL)

    def _load_queries_from_file(self) -> Dict[str, Query]:
        """Load queries from JSON file.

        Supports both formats:
        - Old format: {"id": "q1", "text": "query text"}
        - New format: {"id": "q1", "user_query": "...", "search_query_primary": "...", "search_query_alternate": "..."}
        """
        with open(self.queries_file, "r", encoding="utf-8") as f:
            queries_data = json.load(f)

        queries = {}
        for item in queries_data:
            query_id = item["id"]

            # Support both old and new format
            if "user_query" in item:
                # New format with reformulated queries
                queries[query_id] = Query(
                    id=query_id,
                    text=item["user_query"],
                    search_query_primary=item.get("search_query_primary"),
                    search_query_alternate=item.get("search_query_alternate"),
                    metadata={
                        "category": item.get("category"),
                        "expected_answer": item.get("expected_answer"),
                        "expected_docs": item.get("expected_docs", []),
                        "notes": item.get("notes"),
                    },
                )
            else:
                # Old format (backward compatibility)
                queries[query_id] = Query(
                    id=query_id,
                    text=item["text"],
                    metadata=item.get("metadata", {}),
                )
        return queries

    def _create_default_queries(self) -> Dict[str, Query]:
        """Create default test queries from test cases.

        Note: This creates a basic set. For full evaluation,
        create a queries.json file with all 54 test queries.
        """
        default_queries = [
            ("q1", "who's the PsW PM?"),
            ("q2", "What did I discuss with Ritu in our last 1x1"),
            ("q3", "what are the Q1 '26 must nails"),
            ("q4", "Who is the Group PM manager for Lightroom?"),
            ("q5", "What did Brian and I discuss in our most recent 1x1?"),
        ]

        queries = {}
        for qid, text in default_queries:
            queries[qid] = Query(id=qid, text=text)

        logger.warning(
            f"Using {len(queries)} default queries. "
            "Create queries.json for full test set."
        )
        return queries

    def _load_qrels_from_file(self) -> Dict[str, Dict[str, int]]:
        """Load qrels from JSON file.

        Expected format:
        {
            "q1": {
                "Notes/path/to/doc.md": 2,
                "Notes/another/doc.md": 1
            }
        }
        """
        with open(self.qrels_file, "r", encoding="utf-8") as f:
            return json.load(f)


def load_vault_dataset(
    vault_dir: str = "vault copy",
    queries_file: Optional[str] = None,
    qrels_file: Optional[str] = None,
) -> VaultDataset:
    """Convenience function to load vault dataset.

    Args:
        vault_dir: Directory containing vault markdown files
        queries_file: Path to queries JSON file
        qrels_file: Path to qrels JSON file

    Returns:
        Loaded VaultDataset instance
    """
    dataset = VaultDataset(
        vault_dir=vault_dir,
        queries_file=queries_file,
        qrels_file=qrels_file,
    )
    dataset.load()
    return dataset
