"""Terminal dashboard utilities for TruthChain."""

from __future__ import annotations

from blockchain import Block, Blockchain

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RED = "\033[91m"


def _short(value: str, size: int = 14) -> str:
    return value if len(value) <= size else f"{value[:size]}..."


def render_block(block: Block) -> str:
    integrity = f"{GREEN}intact{RESET}" if not block.is_tampered() else f"{RED}tampered{RESET}"
    verified = block.verified_by if block.verified_by else "pending"
    return (
        f"{BOLD}Block #{block.index}{RESET}\n"
        f"  author: {block.author}\n"
        f"  timestamp: {block.timestamp}\n"
        f"  type: {block.content_type}\n"
        f"  ai_score: {block.ai_score:.2f}\n"
        f"  verified_by: {verified}\n"
        f"  content_hash: {MAGENTA}{_short(block.content_hash, 24)}{RESET}\n"
        f"  previous_hash: {MAGENTA}{_short(block.previous_hash, 24)}{RESET}\n"
        f"  hash: {CYAN}{_short(block.hash, 24)}{RESET}\n"
        f"  integrity: {integrity}\n"
    )


def render_chain(blockchain: Blockchain) -> str:
    header = f"{BOLD}{CYAN}TruthChain Dashboard{RESET}\nChain length: {len(blockchain.chain)}\n"
    body = "\n".join(render_block(block) for block in blockchain.chain)
    valid, message = blockchain.validate_chain()
    status_color = GREEN if valid else RED
    footer = f"{BOLD}Integrity Check:{RESET} {status_color}{message}{RESET}"
    return f"{header}\n{body}\n{footer}"


def print_chain(blockchain: Blockchain) -> None:
    print(render_chain(blockchain))