# Participant Role Definitions and Action Handlers

class Participant:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def perform_action(self, action):
        print(f'{self.name} with role {self.role} is performing action: {action}')


# Define specific participant roles
class Judge(Participant):
    def __init__(self, name):
        super().__init__(name, 'Judge')

    def make_decision(self, decision):
        print(f'Judge {self.name} made a decision: {decision}')


class ParticipantObserver(Participant):
    def __init__(self, name):
        super().__init__(name, 'Observer')

    def give_feedback(self, feedback):
        print(f'Observer {self.name} provides feedback: {feedback}')


# Further implementation of roles and handlers can be added here...