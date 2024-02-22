import numpy as np
from DragonBallEnv import DragonBallEnv
from typing import List, Tuple
import heapdict

FIRST = -2
NO_PREV = -1
class BFSAgent():
    def __init__(self) -> None:
        raise NotImplementedError

    def search(self, env: DragonBallEnv) -> Tuple[List[int], float, int]:
        prev = np.array([FIRST], [NO_PREV] * 63) 
        step_count = 0
        price = 0
        steps_list = []
        reverse_steps_list = []
        open = [(0)]
        close = []
        while (len(open) != 0):
            current = open.pop(0)
            close.append(current)
            for node in succ(self, current):
                open.append(node)
                if (is_final_state(self, node)): #got to the end
                    prev[node[0]] = current
                    while(current[0] != 0):
                        step_count += 1
                        price += self.nL_cost(self.desc[current[0]])
                        reverse_steps_list.append(last_step(self, prev[current], current))
                        current = prev[current]
                    steps_list = reverse_steps_list[::-1] #reverse the reversed tuple
                    return steps_list
                if (prev[node[0]] == NO_PREV):
                    prev[node[0]] = current
           
        raise NotImplementedError


class WeightedAStarAgent():
    def __init__(self) -> None:
        raise NotImplementedError

    def search(self, env: DragonBallEnv, h_weight) -> Tuple[List[int], float, int]:
        raise NotImplementedError



class AStarEpsilonAgent():
    def __init__(self) -> None:
        raise NotImplementedError
        
    def ssearch(self, env: DragonBallEnv, epsilon: int) -> Tuple[List[int], float, int]:
        raise NotImplementedError