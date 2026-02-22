import os
import requests
import colorama
from colorama import Fore, Back, Style
import time

colorama.init()

class Dashboard:
    def __init__(self):
        self.participants = {}
        self.blocks = []
        self.verification_status = False

    def add_participant(self, participant):
        self.participants[participant] = {'activity': [], 'status': 'Active'}

    def update_participant_activity(self, participant, activity):
        if participant in self.participants:
            self.participants[participant]['activity'].append(activity)

    def add_block(self, block):
        self.blocks.append(block)

    def set_verification_status(self, status):
        self.verification_status = status

    def display_dashboard(self):
        os.system('clear')  # Use 'cls' if on Windows
        print(Fore.GREEN + Style.BRIGHT + 'Blockchain Dashboard' + Style.RESET_ALL)  
        print('-' * 50)
        print(Fore.BLUE + 'Current Participants:' + Style.RESET_ALL)
        for participant, info in self.participants.items():
            print(f'{Fore.CYAN}{participant}: {info['status']} - Activities: {info['activity']}{Style.RESET_ALL}')
        print('\n' + Fore.BLUE + 'Blocks:' + Style.RESET_ALL)
        for idx, block in enumerate(self.blocks):
            print(f'{Fore.YELLOW}Block {idx + 1}: {block}{Style.RESET_ALL}')
        print('\n' + Fore.BLUE + f'Verification Status: {Fore.RED}{self.verification_status}{Style.RESET_ALL}')


# Example usage
if __name__ == '__main__':
    dashboard = Dashboard()
    dashboard.add_participant('Alice')
    dashboard.add_participant('Bob')
    dashboard.add_block('Genesis Block')
    dashboard.set_verification_status(True)

    while True:
        dashboard.display_dashboard()
        time.sleep(5)
