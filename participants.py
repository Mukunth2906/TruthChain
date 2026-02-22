"""Participant role simulation for TruthChain."""

from __future__ import annotations

from dataclasses import dataclass

from blockchain import AIResult, Block, Blockchain


def detect_ai_content(text: str) -> AIResult:
    """Offline heuristic AI detector to keep project dependency-free."""
    lower = text.lower()
    ai_markers = (
        "as an ai",
        "in conclusion",
        "furthermore",
        "overall",
        "it is important to note",
        "in summary",
    )
    punctuation_ratio = text.count(",") / max(len(text.split()), 1)
    marker_hits = sum(marker in lower for marker in ai_markers)
    score = min(0.95, 0.2 + marker_hits * 0.12 + punctuation_ratio)

    if score >= 0.65:
        verdict = "Likely AI-generated"
        confidence = "high"
        explanation = "Detected repeated formal transition phrases and machine-like style patterns."
    elif score >= 0.45:
        verdict = "Uncertain / mixed signals"
        confidence = "medium"
        explanation = "Some AI-like patterns found, but not enough for strong attribution."
    else:
        verdict = "Likely human-written"
        confidence = "low"
        explanation = "Language variation appears more organic and less templated."

    return AIResult(
        ai_score=round(score, 4),
        human_score=round(1 - score, 4),
        confidence=confidence,
        verdict=verdict,
        explanation=explanation,
    )


@dataclass
class ContentCreator:
    name: str

    def publish(self, blockchain: Blockchain, content: str) -> tuple[Block, AIResult]:
        ai_result = detect_ai_content(content)
        content_type = "AI-generated" if ai_result.ai_score >= 0.5 else "human-written"
        block = blockchain.add_block(self.name, content, content_type, ai_result.ai_score)
        return block, ai_result


@dataclass
class AITagger:
    name: str

    def tag_content(self, content: str) -> AIResult:
        return detect_ai_content(content)


@dataclass
class FactChecker:
    name: str

    def verify(self, blockchain: Blockchain, block_index: int) -> bool:
        return blockchain.verify_block(block_index, self.name)


@dataclass
class Publisher:
    name: str

    def run_integrity_check(self, blockchain: Blockchain) -> tuple[bool, str]:
        return blockchain.validate_chain()


@dataclass
class EndUser:
    name: str

    def query_provenance(self, blockchain: Blockchain, block_index: int) -> dict | None:
        block = blockchain.get_block(block_index)
        if not block:
            return None
        return {
            "reader": self.name,
            "block_index": block.index,
            "author": block.author,
            "timestamp": block.timestamp,
            "content_type": block.content_type,
            "ai_score": block.ai_score,
            "verified_by": block.verified_by,
            "tamper_proof": not block.is_tampered(),
            "content_hash": block.content_hash,
        }