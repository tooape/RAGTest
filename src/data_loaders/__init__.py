"""Dataset loaders for benchmarking."""

from .base import Dataset, Document, Query, QRel
from .beir_loader import BEIRDataset, load_beir_dataset
from .vault_loader import VaultDataset, load_vault_dataset

__all__ = [
    "Dataset",
    "Document",
    "Query",
    "QRel",
    "BEIRDataset",
    "VaultDataset",
    "load_beir_dataset",
    "load_vault_dataset",
]
