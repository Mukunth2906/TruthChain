# Automated Tamper Attack Simulations

import hashlib
import random
import json

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def calculate_hash(self):
        value = str(self.index) + str(self.previous_hash) + str(self.timestamp) + json.dumps(self.data)
        return hashlib.sha256(value.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(0, '0')  # genesis block

    def create_block(self, index, previous_hash, data=None):
        block = Block(index, previous_hash, int(time.time()), data or {}, '')
        block.hash = block.calculate_hash()
        self.chain.append(block)
        return block

    def tamper_attack(self, block_index, new_data):
        if block_index >= len(self.chain):
            print('Block index out of range')
            return
        self.chain[block_index].data = new_data  # Tamper the block data
        self.chain[block_index].hash = self.chain[block_index].calculate_hash()  # Recalculate hash

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                print(f'Integrity violation at block {current_block.index}')
                return False
            if current_block.previous_hash != previous_block.hash:
                print(f'Hash manipulation detected between blocks {current_block.index} and {previous_block.index}')
                return False
        return True

# Example Usage
if __name__ == '__main__':
    blockchain = Blockchain()
    blockchain.create_block(1, blockchain.chain[-1].hash, {'amount': 10})
    blockchain.create_block(2, blockchain.chain[-1].hash, {'amount': 20})  

    print('Original chain validation:', blockchain.validate_chain())  # Should be True
    blockchain.tamper_attack(1, {'amount': 100})
    print('After tamper attack validation:', blockchain.validate_chain())  # Should be False
    
    
