"""Standalone tamper detection demonstration for TruthChain."""

from blockchain import Blockchain
from participants import ContentCreator, FactChecker, Publisher
from cli_dashboard import print_chain


def run_demo() -> None:
    chain = Blockchain()

    creator = ContentCreator("Alice")
    creator.publish(
        chain,
        "Breaking report: Satellite imagery confirms heavy flooding in the delta region.",
    )
    creator.publish(
        chain,
        "In conclusion, this response uses structured phrasing and overall polished transitions.",
    )

    checker = FactChecker("Dr. Veritas")
    checker.verify(chain, 1)

    publisher = Publisher("TruthTimes")
    valid_before, msg_before = publisher.run_integrity_check(chain)
    print(f"Before tampering: {valid_before} ({msg_before})")

    victim = chain.get_block(1)
    if victim:
        victim.content = "Tampered payload: Deepfake content inserted retroactively."
        victim.content_hash = "0" * 64

    valid_after, msg_after = publisher.run_integrity_check(chain)
    print(f"After tampering: {valid_after} ({msg_after})")

    print_chain(chain)


if __name__ == "__main__":
    run_demo()