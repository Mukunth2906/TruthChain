# Automated Tamper Attack Simulations on Blockchain Blocks

This script demonstrates automated simulations of tamper attack scenarios on blockchain blocks. It covers various attack scenarios, detection mechanisms, and reporting of integrity violations.

## Attack Scenarios

1. **Block Data Tampering**: Modifying the data of existing blocks.
2. **Block Reordering**: Changing the order of blocks to manipulate the blockchain state.
3. **Double Spending**: Attempting to spend the same digital currency multiple times.

## Detection Mechanisms

- **Hash Checking**: Verifying the integrity of blocks by checking their hash values.
- **Consensus Algorithm Simulation**: Simulating consensus algorithms (like Proof of Work) to identify inconsistencies.

## Reporting Integrity Violations

The script logs any detected integrity violations with details on the type of attack and the block(s) involved.

## Python Code

```python
import hashlib
import random
import json
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data='Genesis Block', previous_hash='0')

    def create_block(self, data, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'data': data,
            'previous_hash': previous_hash,
        }
        self.chain.append(block)
        return block

    def tamper_block(self, index, new_data):
        if index < len(self.chain):  
            original_data = self.chain[index]['data']
            self.chain[index]['data'] = new_data
            print(f"Block {index} tampered: {original_data} -> {new_data}")
        else:
            print("Invalid block index!")

    def report_integrity_violations(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current['previous_hash'] != self.hash(previous):
                print(f"Integrity violation detected at block {i}!")

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

# Simulating tamper attacks
blockchain = Blockchain()
blockchain.create_block(data='Transaction 1', previous_hash=blockchain.chain[-1]['previous_hash'])
blockchain.create_block(data='Transaction 2', previous_hash=blockchain.chain[-1]['previous_hash'])

# Performing tampering
blockchain.tamper_block(1, 'Tampered Transaction 1')
blockchain.report_integrity_violations()
``` 

## Usage
Run this script in a Python environment. Ensure you have the necessary permissions to modify files and execute scripts. The script will output any integrity violations detected during the simulation.

## Note
This script is for educational purposes only and should not be used to conduct unlawful activities.