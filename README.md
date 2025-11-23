# RAG Test Repository

This repository contains test datasets for RAG (Retrieval-Augmented Generation) evaluation.

## Test Cases

For test case documentation, see: [Test Cases](obsidian://open?vault=My%20Vault&file=Notes%2FMisc%2FCode%20Projects%2FcustomRAG%2FTest%20cases)

## Datasets

### Vault Copy
- **vault copy/**: Snapshot of Obsidian vault content for testing

### BEIR Datasets

**Note**: Datasets are not included in this repository due to size (~3.6GB total). Download them locally using the provided script.

#### Download Instructions
```bash
# Install beir library
pip install beir

# Download datasets
python3 download_beir.py
```

This will download:
- **beir_datasets/nq/**: Natural Questions dataset (3.4k queries, 2.7M passages, ~1.5GB)
- **beir_datasets/hotpotqa/**: HotpotQA dataset (7.4k queries, 5.2M passages, ~2.1GB)

## Testing Strategy

### Phase 1: Candidate Evaluation with BEIR
1. Create a list of candidate query strategies
2. Test each strategy against BEIR query sets (NQ and HotpotQA)
3. Run multiple permutations of hyperparameters for each strategy
4. Evaluate performance using standard IR metrics (MRR, NDCG, Recall@k)

### Phase 2: Top Candidates Validation
1. Select top 3 performing strategies from Phase 1
2. Test these candidates against the vault copy dataset
3. Validate performance on domain-specific queries
4. Select final strategy based on combined BEIR + vault performance
