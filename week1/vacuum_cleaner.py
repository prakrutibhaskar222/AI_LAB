"""
Vacuum Cleaner World - AI Lab Program
--------------------------------------
Classic AI agent problem: a two-location "vacuum world" (Location A and
Location B), each of which may be Clean or Dirty. A simple reflex agent
perceives its current location and its cleanliness status, and acts
according to a fixed rule table (no memory of the past, no search).

Percept  : (location, status)
Actions  : 'Suck', 'Left', 'Right', 'NoOp'

Agent function (simple reflex agent):
    if status == Dirty:      Suck
    elif location == A:      Right
    elif location == B:      Left

This program also reports total moves and a performance measure
(a +1 score awarded each time step a location is clean, and a small
penalty for each action taken).
"""

import random
print("SCRIPT STARTED")

LOCATIONS = ['A', 'B']


# ---------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------

class VacuumEnvironment:
    def __init__(self, status_A=None, status_B=None):
        self.status = {
            'A': status_A if status_A else random.choice(['Clean', 'Dirty']),
            'B': status_B if status_B else random.choice(['Clean', 'Dirty']),
        }
        self.agent_location = random.choice(LOCATIONS)
        self.performance = 0

    def percept(self):
        return (self.agent_location, self.status[self.agent_location])

    def execute_action(self, action):
        if action == 'Suck':
            if self.status[self.agent_location] == 'Dirty':
                self.status[self.agent_location] = 'Clean'
        elif action == 'Right':
            self.agent_location = 'B'
            self.performance -= 1  # cost of moving
        elif action == 'Left':
            self.agent_location = 'A'
            self.performance -= 1  # cost of moving
        elif action == 'NoOp':
            pass

        # Reward: +1 for every location currently clean this time step
        for loc in LOCATIONS:
            if self.status[loc] == 'Clean':
                self.performance += 1

    def is_all_clean(self):
        return all(status == 'Clean' for status in self.status.values())

    def display(self):
        print(f"  Location A: {self.status['A']:6s} | "
              f"Location B: {self.status['B']:6s} | "
              f"Agent at: {self.agent_location}")


# ---------------------------------------------------------------------
# Simple Reflex Agent
# ---------------------------------------------------------------------

def simple_reflex_agent(percept):
    location, status = percept
    if status == 'Dirty':
        return 'Suck'
    elif location == 'A':
        return 'Right'
    elif location == 'B':
        return 'Left'
    return 'NoOp'


# ---------------------------------------------------------------------
# Run the agent in the environment
# ---------------------------------------------------------------------

def run_agent(env, agent_program, max_steps=10):
    print("Initial state:")
    env.display()
    print()

    step = 0
    while step < max_steps:
        percept = env.percept()
        action = agent_program(percept)
        print(f"Step {step + 1}: Percept={percept} -> Action='{action}'")

        env.execute_action(action)
        env.display()

        if env.is_all_clean() and action != 'Suck':
            # Both clean and agent chose to move (or NoOp) -> done
            print("\nBoth locations clean. Stopping.")
            break

        step += 1
        print()

    print(f"\nFinal performance measure: {env.performance}")
    print(f"Total steps taken: {step + 1}")


if __name__ == "__main__":
    print("=" * 60)
    print("VACUUM CLEANER WORLD - Simple Reflex Agent")
    print("=" * 60)

    # You can fix the initial state for reproducible testing, e.g.:
    # env = VacuumEnvironment(status_A='Dirty', status_B='Dirty')
    env = VacuumEnvironment()

    run_agent(env, simple_reflex_agent, max_steps=10)