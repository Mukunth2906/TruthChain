# Comprehensive Participant Role Classes for TruthChain

class ContentCreator:
    def __init__(self, name):
        self.name = name

    def publish_content(self, content):
        # Logic to publish content to the blockchain
        print(f"Content published by {self.name}: {content}")

class AITagger:
    def __init__(self, name):
        self.name = name

    def detect_ai(self, content):
        # Logic to detect AI-generated content
        print(f"AI detection by {self.name}: {content}")

class FactChecker:
    def __init__(self, name):
        self.name = name

    def verify_block(self, block):
        # Logic to verify the integrity of a blockchain block
        print(f"Block verification by {self.name}: {block}")

class Publisher:
    def __init__(self, name):
        self.name = name

    def check_integrity(self, content):
        # Logic to check content integrity
        print(f"Integrity check by {self.name}: {content}")

class EndUser:
    def __init__(self, name):
        self.name = name

    def query_provenance(self, content):
        # Logic to query content provenance
        print(f"Provenance query by {self.name}: {content}")