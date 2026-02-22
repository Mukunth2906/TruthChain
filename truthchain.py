"""Main interactive CLI for TruthChain."""

from __future__ import annotations

from blockchain import Blockchain
from cli_dashboard import print_chain
from participants import ContentCreator, EndUser, FactChecker, Publisher


def _input_multiline() -> str:
    print("Paste content. Submit an empty line to finish:")
    lines: list[str] = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def run() -> None:
    chain = Blockchain()

    while True:
        print(
            "\n=== TruthChain Menu ===\n"
            "1) Publish content (Creator)\n"
            "2) Verify a block (Fact Checker)\n"
            "3) Check chain integrity (Publisher)\n"
            "4) Query provenance (End User)\n"
            "5) View full dashboard\n"
            "6) Simulate tamper attack\n"
            "0) Exit"
        )
        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Creator name: ").strip() or "Anonymous Creator"
            content = _input_multiline()
            if not content:
                print("No content entered.")
                continue
            creator = ContentCreator(name)
            block, ai_result = creator.publish(chain, content)
            print(
                f"Block #{block.index} published. "
                f"AI score: {ai_result.ai_score:.2f} ({ai_result.verdict})"
            )

        elif choice == "2":
            name = input("Fact checker name: ").strip() or "Verifier"
            try:
                index = int(input("Block index to verify: ").strip())
            except ValueError:
                print("Invalid number.")
                continue
            checker = FactChecker(name)
            if checker.verify(chain, index):
                print("Block verified.")
            else:
                print("Block verification failed.")

        elif choice == "3":
            name = input("Publisher/platform name: ").strip() or "Publisher"
            publisher = Publisher(name)
            valid, message = publisher.run_integrity_check(chain)
            print(f"Integrity result: {valid} ({message})")

        elif choice == "4":
            name = input("Reader name: ").strip() or "Reader"
            try:
                index = int(input("Block index to query: ").strip())
            except ValueError:
                print("Invalid number.")
                continue
            reader = EndUser(name)
            report = reader.query_provenance(chain, index)
            if not report:
                print("Invalid block index.")
            else:
                for key, value in report.items():
                    print(f"{key}: {value}")

        elif choice == "5":
            print_chain(chain)

        elif choice == "6":
            try:
                index = int(input("Block index to tamper: ").strip())
            except ValueError:
                print("Invalid number.")
                continue
            block = chain.get_block(index)
            if not block or index == 0:
                print("Invalid block index.")
            else:
                forged = input("Injected fake content: ").strip()
                block.content = forged
                block.content_hash = "forged-content-hash"
                print("Tampering completed. Run integrity check to see detection.")

        elif choice == "0":
            print("Goodbye from TruthChain.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    run()