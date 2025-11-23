"""
Tests for dataset loaders.

This module tests:
1. Base dataset classes (Document, Query, QRel, Dataset)
2. BEIR dataset loader
3. Vault dataset loader
4. Dataset validation and error handling
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

import pytest

from src.datasets.base import Document, Query, QRel, Dataset
from src.datasets.beir_loader import BEIRDataset


class TestDocumentDataclass:
    """Test Document dataclass."""

    def test_document_creation(self):
        """Test creating a document."""
        doc = Document(id="doc1", text="This is a test document")

        assert doc.id == "doc1"
        assert doc.text == "This is a test document"
        assert doc.metadata is None

    def test_document_with_metadata(self):
        """Test creating a document with metadata."""
        doc = Document(
            id="doc1",
            text="Test text",
            metadata={"title": "Test Title", "author": "Test Author"}
        )

        assert doc.metadata["title"] == "Test Title"
        assert doc.metadata["author"] == "Test Author"

    def test_document_repr(self):
        """Test document string representation."""
        doc = Document(id="doc1", text="Short text")
        repr_str = repr(doc)

        assert "doc1" in repr_str
        assert "Short text" in repr_str

    def test_document_repr_long_text(self):
        """Test document repr with long text."""
        long_text = "a" * 100
        doc = Document(id="doc1", text=long_text)
        repr_str = repr(doc)

        # Should be truncated
        assert len(repr_str) < len(long_text) + 50
        assert "..." in repr_str


class TestQueryDataclass:
    """Test Query dataclass."""

    def test_query_creation(self):
        """Test creating a query."""
        query = Query(id="q1", text="What is the capital of France?")

        assert query.id == "q1"
        assert query.text == "What is the capital of France?"
        assert query.metadata is None

    def test_query_with_metadata(self):
        """Test creating a query with metadata."""
        query = Query(
            id="q1",
            text="Test query",
            metadata={"type": "factoid"}
        )

        assert query.metadata["type"] == "factoid"

    def test_query_repr(self):
        """Test query string representation."""
        query = Query(id="q1", text="Test query")
        repr_str = repr(query)

        assert "q1" in repr_str
        assert "Test query" in repr_str


class TestQRelDataclass:
    """Test QRel dataclass."""

    def test_qrel_creation(self):
        """Test creating a qrel."""
        qrel = QRel(query_id="q1", doc_id="doc1", relevance=2)

        assert qrel.query_id == "q1"
        assert qrel.doc_id == "doc1"
        assert qrel.relevance == 2

    def test_qrel_repr(self):
        """Test qrel string representation."""
        qrel = QRel(query_id="q1", doc_id="doc1", relevance=1)
        repr_str = repr(qrel)

        assert "q1" in repr_str
        assert "doc1" in repr_str
        assert "1" in repr_str


class TestBaseDatasetAbstract:
    """Test base Dataset abstract class."""

    def test_dataset_must_implement_load(self):
        """Test that Dataset subclasses must implement load()."""
        with pytest.raises(TypeError):
            # Can't instantiate abstract class without implementing load()
            dataset = Dataset("test")

    def test_dataset_name(self):
        """Test dataset name attribute."""
        # Create a concrete implementation for testing
        class ConcreteDataset(Dataset):
            def load(self):
                self._corpus = {}
                self._queries = {}
                self._qrels = {}

        dataset = ConcreteDataset("test_dataset")
        assert dataset.name == "test_dataset"

    def test_dataset_properties_before_load(self):
        """Test accessing properties before loading raises error."""
        class ConcreteDataset(Dataset):
            def load(self):
                self._corpus = {}
                self._queries = {}
                self._qrels = {}

        dataset = ConcreteDataset("test")

        with pytest.raises(ValueError, match="Dataset not loaded"):
            _ = dataset.corpus

        with pytest.raises(ValueError, match="Dataset not loaded"):
            _ = dataset.queries

        with pytest.raises(ValueError, match="Dataset not loaded"):
            _ = dataset.qrels

    def test_dataset_properties_after_load(self):
        """Test accessing properties after loading."""
        class ConcreteDataset(Dataset):
            def load(self):
                self._corpus = {"doc1": Document(id="doc1", text="Test")}
                self._queries = {"q1": Query(id="q1", text="Query")}
                self._qrels = {"q1": {"doc1": 1}}

        dataset = ConcreteDataset("test")
        dataset.load()

        assert len(dataset.corpus) == 1
        assert len(dataset.queries) == 1
        assert len(dataset.qrels) == 1

    def test_get_relevant_docs(self):
        """Test getting relevant documents for a query."""
        class ConcreteDataset(Dataset):
            def load(self):
                self._corpus = {}
                self._queries = {}
                self._qrels = {
                    "q1": {"doc1": 2, "doc2": 1, "doc3": 0}
                }

        dataset = ConcreteDataset("test")
        dataset.load()

        # All relevant (min_relevance=1)
        relevant = dataset.get_relevant_docs("q1", min_relevance=1)
        assert relevant == {"doc1", "doc2"}

        # Highly relevant only (min_relevance=2)
        highly_relevant = dataset.get_relevant_docs("q1", min_relevance=2)
        assert highly_relevant == {"doc1"}

    def test_get_relevant_docs_nonexistent_query(self):
        """Test getting relevant docs for nonexistent query."""
        class ConcreteDataset(Dataset):
            def load(self):
                self._corpus = {}
                self._queries = {}
                self._qrels = {}

        dataset = ConcreteDataset("test")
        dataset.load()

        relevant = dataset.get_relevant_docs("nonexistent")
        assert relevant == set()

    def test_dataset_repr_before_load(self):
        """Test dataset repr before loading."""
        class ConcreteDataset(Dataset):
            def load(self):
                pass

        dataset = ConcreteDataset("test")
        repr_str = repr(dataset)

        assert "test" in repr_str
        assert "loaded=False" in repr_str

    def test_dataset_repr_after_load(self):
        """Test dataset repr after loading."""
        class ConcreteDataset(Dataset):
            def load(self):
                self._corpus = {"doc1": Document(id="doc1", text="Test")}
                self._queries = {"q1": Query(id="q1", text="Query")}
                self._qrels = {"q1": {"doc1": 1}}

        dataset = ConcreteDataset("test")
        dataset.load()
        repr_str = repr(dataset)

        assert "test" in repr_str
        assert "docs=1" in repr_str
        assert "queries=1" in repr_str


class TestBEIRDatasetInitialization:
    """Test BEIR dataset initialization."""

    def test_beir_dataset_init(self):
        """Test BEIR dataset initialization."""
        dataset = BEIRDataset(
            name="nq",
            data_dir="test_data",
            split="test"
        )

        assert dataset.name == "nq"
        assert dataset.split == "test"
        assert "test_data" in str(dataset.dataset_path)

    def test_beir_dataset_default_params(self):
        """Test BEIR dataset with default parameters."""
        dataset = BEIRDataset(name="nq")

        assert dataset.split == "test"
        assert "beir_datasets" in str(dataset.data_dir)


class TestBEIRDatasetLoading:
    """Test BEIR dataset loading functionality."""

    def test_load_corpus(self, tmp_path):
        """Test loading corpus from JSONL file."""
        # Create test corpus file
        corpus_file = tmp_path / "corpus.jsonl"
        corpus_data = [
            {"_id": "doc1", "title": "Title 1", "text": "Content 1"},
            {"_id": "doc2", "title": "", "text": "Content 2"},
            {"_id": "doc3", "text": "Content 3"}  # No title
        ]

        with open(corpus_file, "w") as f:
            for doc in corpus_data:
                f.write(json.dumps(doc) + "\n")

        dataset = BEIRDataset(name="test", data_dir=str(tmp_path))
        corpus = dataset._load_corpus(corpus_file)

        assert len(corpus) == 3
        assert corpus["doc1"].text == "Title 1 Content 1"
        assert corpus["doc2"].text == "Content 2"
        assert corpus["doc3"].text == "Content 3"
        assert corpus["doc1"].metadata["title"] == "Title 1"

    def test_load_queries(self, tmp_path):
        """Test loading queries from JSONL file."""
        # Create test queries file
        queries_file = tmp_path / "queries.jsonl"
        queries_data = [
            {"_id": "q1", "text": "Query 1"},
            {"_id": "q2", "text": "Query 2"}
        ]

        with open(queries_file, "w") as f:
            for query in queries_data:
                f.write(json.dumps(query) + "\n")

        dataset = BEIRDataset(name="test", data_dir=str(tmp_path))
        queries = dataset._load_queries(queries_file)

        assert len(queries) == 2
        assert queries["q1"].text == "Query 1"
        assert queries["q2"].text == "Query 2"

    def test_load_qrels(self, tmp_path):
        """Test loading qrels from TSV file."""
        # Create test qrels file
        qrels_file = tmp_path / "qrels.tsv"
        qrels_content = """query-id\tcorpus-id\tscore
q1\tdoc1\t2
q1\tdoc2\t1
q2\tdoc3\t1
"""
        with open(qrels_file, "w") as f:
            f.write(qrels_content)

        dataset = BEIRDataset(name="test", data_dir=str(tmp_path))
        qrels = dataset._load_qrels(qrels_file)

        assert len(qrels) == 2
        assert qrels["q1"]["doc1"] == 2
        assert qrels["q1"]["doc2"] == 1
        assert qrels["q2"]["doc3"] == 1

    def test_load_full_dataset(self, tmp_path):
        """Test loading a complete BEIR dataset."""
        # Create dataset directory structure
        dataset_path = tmp_path / "nq"
        dataset_path.mkdir()
        qrels_dir = dataset_path / "qrels"
        qrels_dir.mkdir()

        # Create corpus
        corpus_file = dataset_path / "corpus.jsonl"
        with open(corpus_file, "w") as f:
            f.write(json.dumps({"_id": "doc1", "title": "Doc 1", "text": "Content 1"}) + "\n")

        # Create queries
        queries_file = dataset_path / "queries.jsonl"
        with open(queries_file, "w") as f:
            f.write(json.dumps({"_id": "q1", "text": "Query 1"}) + "\n")

        # Create qrels
        qrels_file = qrels_dir / "test.tsv"
        with open(qrels_file, "w") as f:
            f.write("query-id\tcorpus-id\tscore\n")
            f.write("q1\tdoc1\t1\n")

        # Load dataset
        dataset = BEIRDataset(name="nq", data_dir=str(tmp_path))
        dataset.load()

        assert len(dataset.corpus) == 1
        assert len(dataset.queries) == 1
        assert len(dataset.qrels) == 1

    def test_load_nonexistent_dataset(self):
        """Test loading a nonexistent dataset raises error."""
        dataset = BEIRDataset(name="nonexistent", data_dir="/tmp/nonexistent")

        with pytest.raises(FileNotFoundError, match="Dataset not found"):
            dataset.load()


class TestBEIRDatasetFunctionality:
    """Test BEIR dataset functionality."""

    def test_dataset_get_relevant_docs_integration(self, tmp_path):
        """Test getting relevant docs after loading BEIR dataset."""
        # Create minimal dataset
        dataset_path = tmp_path / "test_dataset"
        dataset_path.mkdir()
        qrels_dir = dataset_path / "qrels"
        qrels_dir.mkdir()

        # Create files
        corpus_file = dataset_path / "corpus.jsonl"
        with open(corpus_file, "w") as f:
            f.write(json.dumps({"_id": "doc1", "text": "Doc 1"}) + "\n")
            f.write(json.dumps({"_id": "doc2", "text": "Doc 2"}) + "\n")

        queries_file = dataset_path / "queries.jsonl"
        with open(queries_file, "w") as f:
            f.write(json.dumps({"_id": "q1", "text": "Query 1"}) + "\n")

        qrels_file = qrels_dir / "test.tsv"
        with open(qrels_file, "w") as f:
            f.write("query-id\tcorpus-id\tscore\n")
            f.write("q1\tdoc1\t2\n")
            f.write("q1\tdoc2\t1\n")

        # Load and test
        dataset = BEIRDataset(name="test_dataset", data_dir=str(tmp_path))
        dataset.load()

        relevant = dataset.get_relevant_docs("q1", min_relevance=1)
        assert relevant == {"doc1", "doc2"}


class TestDatasetErrorHandling:
    """Test dataset error handling."""

    def test_corpus_property_error(self):
        """Test corpus property raises error before load."""
        class TestDataset(Dataset):
            def load(self):
                pass

        dataset = TestDataset("test")

        with pytest.raises(ValueError, match="Dataset not loaded"):
            _ = dataset.corpus

    def test_queries_property_error(self):
        """Test queries property raises error before load."""
        class TestDataset(Dataset):
            def load(self):
                pass

        dataset = TestDataset("test")

        with pytest.raises(ValueError, match="Dataset not loaded"):
            _ = dataset.queries

    def test_qrels_property_error(self):
        """Test qrels property raises error before load."""
        class TestDataset(Dataset):
            def load(self):
                pass

        dataset = TestDataset("test")

        with pytest.raises(ValueError, match="Dataset not loaded"):
            _ = dataset.qrels


class TestBEIRLoaderFunction:
    """Test BEIR loader utility function."""

    def test_load_beir_dataset_function(self, tmp_path):
        """Test the load_beir_dataset utility function."""
        from src.datasets.beir_loader import load_beir_dataset

        # Create minimal dataset
        dataset_path = tmp_path / "test_ds"
        dataset_path.mkdir()
        qrels_dir = dataset_path / "qrels"
        qrels_dir.mkdir()

        # Create files
        corpus_file = dataset_path / "corpus.jsonl"
        with open(corpus_file, "w") as f:
            f.write(json.dumps({"_id": "doc1", "text": "Doc 1"}) + "\n")

        queries_file = dataset_path / "queries.jsonl"
        with open(queries_file, "w") as f:
            f.write(json.dumps({"_id": "q1", "text": "Query 1"}) + "\n")

        qrels_file = qrels_dir / "test.tsv"
        with open(qrels_file, "w") as f:
            f.write("query-id\tcorpus-id\tscore\n")
            f.write("q1\tdoc1\t1\n")

        # Load using utility function
        dataset = load_beir_dataset("test_ds", data_dir=str(tmp_path))

        assert isinstance(dataset, BEIRDataset)
        assert len(dataset.corpus) == 1
        assert len(dataset.queries) == 1


class TestVaultDatasetBasics:
    """Test Vault dataset basic functionality."""

    def test_vault_dataset_import(self):
        """Test that VaultDataset can be imported."""
        from src.datasets.vault_loader import VaultDataset

        assert VaultDataset is not None

    def test_vault_load_function_import(self):
        """Test that load_vault_dataset can be imported."""
        from src.datasets.vault_loader import load_vault_dataset

        assert load_vault_dataset is not None

    def test_vault_dataset_initialization(self):
        """Test VaultDataset initialization."""
        from src.datasets.vault_loader import VaultDataset

        dataset = VaultDataset(
            name="test_vault",
            vault_path="/path/to/vault"
        )

        assert dataset.name == "test_vault"
        assert "/path/to/vault" in str(dataset.vault_path)


class TestDatasetComparison:
    """Test dataset comparison and utilities."""

    def test_document_equality(self):
        """Test document equality comparison."""
        doc1 = Document(id="doc1", text="Test")
        doc2 = Document(id="doc1", text="Test")
        doc3 = Document(id="doc2", text="Test")

        assert doc1 == doc2
        assert doc1 != doc3

    def test_query_equality(self):
        """Test query equality comparison."""
        q1 = Query(id="q1", text="Query")
        q2 = Query(id="q1", text="Query")
        q3 = Query(id="q2", text="Query")

        assert q1 == q2
        assert q1 != q3

    def test_qrel_equality(self):
        """Test qrel equality comparison."""
        qrel1 = QRel(query_id="q1", doc_id="doc1", relevance=1)
        qrel2 = QRel(query_id="q1", doc_id="doc1", relevance=1)
        qrel3 = QRel(query_id="q1", doc_id="doc2", relevance=1)

        assert qrel1 == qrel2
        assert qrel1 != qrel3
