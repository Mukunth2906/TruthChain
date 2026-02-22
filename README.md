# TruthChain

## ⛓️ Blockchain-Based AI Content Provenance & Accountability System

TruthChain is a lightweight blockchain simulation that records digital content origin, AI-likelihood, and verification actions in a tamper-evident chain.

## Problem

Online content is hard to trust. We often cannot answer:
- Who created this content?
- Was it AI-generated?
- Was it modified later?

## Solution

TruthChain stores content metadata on a chained ledger where each block includes:
- content hash
- author identity
- AI score and content type
- verification status
- linked previous hash

Any post-publication modification breaks integrity checks.

## Participants

1. **Content Creator** – submits content to the chain.
2. **AI Tagger** – assigns an AI-likelihood score.
3. **Fact Checker** – verifies a block before approval.
4. **Publisher** – validates full chain integrity.
5. **End User** – queries provenance for a block.

## Block Structure

```text
Block {
  index
  timestamp
  author
  content
  content_hash
  content_type
  ai_score
  verified_by
  previous_hash
  hash
}
truthchain/
├── blockchain.py      # Core block + blockchain classes
├── participants.py    # Participant roles and actions
├── cli_dashboard.py   # Colored terminal dashboard rendering
├── tamper_demo.py     # End-to-end tamper detection demo
├── truthchain.py      # Interactive CLI application
├── requirements.txt   # Optional dependencies (none required)
└── README.md