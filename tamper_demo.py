# Tamper Attack Demonstration

"""
This script demonstrates automated tamper attack scenarios and detection mechanisms.
"""

import random
import time

class TamperSimulation:
    def __init__(self):
        self.data = "Sensitive Data"

    def automated_tampering(self):
        return random.choice(["Tampered Data", self.data])

    def detect_tampering(self, received_data):
        if received_data == self.data:
            return "No Tampering Detected"
        else:
            return "Tampering Detected!"

if __name__ == '__main__':
    simulation = TamperSimulation()
    while True:
        tampered_data = simulation.automated_tampering()
        print(f"Received Data: {tampered_data}")
        print(simulation.detect_tampering(tampered_data))
        time.sleep(2)  # Simulate time between attacks
