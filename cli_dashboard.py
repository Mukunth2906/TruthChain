import os
import time
import random

class ChainDashboard:
    def __init__(self):
        self.participants = []
        self.blocks = []
        self.verification_status = 'Pending'

    def add_participant(self, participant):
        self.participants.append(participant)

    def add_block(self, block):
        self.blocks.append(block)

    def update_verification_status(self, status):
        self.verification_status = status

    def display_dashboard(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\033[1;34;40mEnhanced Chain Dashboard\033[0m')
        print('\033[1;32;40mCurrent Participants:\033[0m')
        for p in self.participants:
            print(f' - {p}')
        print('\033[1;33;40mCurrent Blocks:\033[0m')
        for b in self.blocks:
            print(f' - Block Data: {b}')
        print(f'\033[1;35;40mVerification Status: {self.verification_status}\033[0m')

    def simulate_activity(self):
        while True:
            self.add_participant(f'Participant {random.randint(1, 100)}')
            self.add_block(f'Block {random.randint(1, 1000)}')
            self.update_verification_status(random.choice(['Pending', 'Verified', 'Failed']))
            self.display_dashboard()
            time.sleep(5)

if __name__ == '__main__':
    dashboard = ChainDashboard()
    dashboard.simulate_activity()