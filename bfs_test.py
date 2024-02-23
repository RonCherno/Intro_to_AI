from DragonBallEnv import DragonBallEnv
from typing import List, Tuple
from Algorithms import *

DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3

MAPS = {
    "2x2": ["DF",
            "DG"],

    "4x4": ["SFFF",
            "FDFF",
            "FFFD",
            "FFFG"],
    "8x8": [
        "SFFFFFFF",
        "FFFFFTAL",
        "TFFHFFTF",
        "FFFFFHTF",
        "FAFHFFFF",
        "FHHFFFHF",
        "DFTFHDTL",
        "FLFHFFFG",
    ],
}


env = DragonBallEnv(MAPS["2x2"])
state = env.reset()
print('Initial state:', state)
print('Goal states:', env.goals) 
print(f"Action Space {env.action_space}")
print(f"State Space {env.observation_space}")
print(env.render())

BFS_agent = BFSAgent()
actions, total_cost, expanded = BFS_agent.search(env)
print(f"Total_cost: {total_cost}")
print(f"Expanded: {expanded}")
print(f"Actions: {actions}")

assert total_cost == 119.0, "Error in total cost returned"