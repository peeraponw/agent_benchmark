# Pre-computed Embeddings Directory

This directory will contain pre-computed vector embeddings for the RAG documents to ensure consistency across framework comparisons.

## Structure

- `document_embeddings.json` - Vector embeddings for each document chunk
- `embedding_metadata.json` - Information about the embedding model and parameters used
- `chunk_mappings.json` - Mapping between chunks and their source documents

## Usage

Frameworks should use these pre-computed embeddings when available to ensure fair comparison. If embeddings need to be regenerated, use consistent parameters:

- Model: sentence-transformers/all-MiniLM-L6-v2 (or specified in metadata)
- Chunk size: 512 tokens with 50 token overlap
- Normalization: L2 normalized vectors

## Notes

This is a placeholder directory. Actual embeddings will be generated during the test data preparation phase.
