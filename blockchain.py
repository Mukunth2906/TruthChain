"""Core blockchain primitives for TruthChain."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any


@dataclass
class AIResult:
    ai_score: float
    human_score: float
    confidence: str
    verdict: str
    explanation: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "ai_score": round(self.ai_score, 4),
            "human_score": round(self.human_score, 4),
            "confidence": self.confidence,
            "verdict": self.verdict,
            "explanation": self.explanation,
        }


@dataclass
class Block:
    index: int
    author: str
    content: str
    content_type: str
    ai_score: float
    previous_hash: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    verified_by: str | None = None
    content_hash: str = field(init=False)
    hash: str = field(init=False)

    def __post_init__(self) -> None:
        self.content_hash = hashlib.sha256(self.content.encode("utf-8")).hexdigest()
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "author": self.author,
            "content_hash": self.content_hash,
            "content_type": self.content_type,
            "ai_score": self.ai_score,
            "previous_hash": self.previous_hash,
        }
        canonical = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def is_tampered(self) -> bool:
        return self.hash != self.calculate_hash()

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "author": self.author,
            "content": self.content,
            "content_hash": self.content_hash,
            "content_type": self.content_type,
            "ai_score": self.ai_score,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }


class Blockchain:
    def __init__(self) -> None:
        self.chain: list[Block] = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        genesis = Block(
            index=0,
            author="TruthChain System",
            content="Genesis Block - TruthChain Initialized",
            content_type="system",
            ai_score=0.0,
            previous_hash="0" * 64,
        )
        genesis.verified_by = "system"
        genesis.hash = genesis.calculate_hash()
        self.chain.append(genesis)

    @property
    def latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, author: str, content: str, content_type: str, ai_score: float) -> Block:
        block = Block(
            index=len(self.chain),
            author=author,
            content=content,
            content_type=content_type,
            ai_score=ai_score,
            previous_hash=self.latest_block.hash,
        )
        self.chain.append(block)
        return block

    def get_block(self, index: int) -> Block | None:
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def verify_block(self, index: int, verifier: str) -> bool:
        block = self.get_block(index)
        if block is None or block.index == 0 or block.verified_by:
            return False
        if block.is_tampered():
            return False
        block.verified_by = verifier
        block.hash = block.calculate_hash()
        return True

    def validate_chain(self) -> tuple[bool, str]:
        for index in range(1, len(self.chain)):
            current = self.chain[index]
            previous = self.chain[index - 1]
            if current.is_tampered():
                return False, f"Block #{current.index} hash mismatch"
            if current.previous_hash != previous.hash:
                return False, f"Block #{current.index} previous hash mismatch"
        return True, "Chain integrity verified"

    def to_json(self) -> str:
        return json.dumps([block.to_dict() for block in self.chain], indent=2)
