#!/usr/bin/env python3
"""Download BEIR datasets for RAG testing.

This script downloads the NQ and HotpotQA datasets from the BEIR benchmark.
Datasets are saved to the beir_datasets/ directory.

Requirements:
    pip install beir

Usage:
    python3 download_beir.py
"""

from beir import util
import os

# Create datasets directory
datasets_dir = "beir_datasets"
os.makedirs(datasets_dir, exist_ok=True)

# Download NQ (Natural Questions)
print("Downloading Natural Questions dataset...")
nq_url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nq.zip"
nq_path = util.download_and_unzip(nq_url, datasets_dir)
print(f"✓ NQ downloaded to: {nq_path}")

# Download HotpotQA
print("\nDownloading HotpotQA dataset...")
hotpotqa_url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/hotpotqa.zip"
hotpotqa_path = util.download_and_unzip(hotpotqa_url, datasets_dir)
print(f"✓ HotpotQA downloaded to: {hotpotqa_path}")

print("\n✓ Download complete!")
print("\nDataset structure:")
print("  beir_datasets/")
print("  ├── nq/")
print("  │   ├── corpus.jsonl       (2.7M passages)")
print("  │   ├── queries.jsonl      (3.4k queries)")
print("  │   └── qrels/")
print("  └── hotpotqa/")
print("      ├── corpus.jsonl       (5.2M passages)")
print("      ├── queries.jsonl      (7.4k queries)")
print("      └── qrels/")
