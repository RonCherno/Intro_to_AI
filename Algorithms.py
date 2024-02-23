import numpy as np
from DragonBallEnv import DragonBallEnv
from typing import List, Tuple
import heapdict

FIRST = -2
NO_PREV = -1
ALL_BALLS = 2

class Node():
    def __init__(self, f: int, num_state: int, actions: list, cost: int, terminated: bool, d1_status: bool, d2_status: bool) -> None:
        self.c_f = f
        self.c_num_state = num_state
        self.c_actions = actions.copy()
        self.c_total_cost = cost
        self.c_terminated = terminated
        self.c_d1_status = d1_status
        self.c_d2_status = d2_status
    def __eq__ (self, other):
        return (self.c_f, self.c_num_state)==(other.c_f, other.c_num_state)
    def __lt__ (self, other):
        return (self.c_f, self.c_num_state)<(other.c_f, other.c_num_state)
    


""" BFS"""

class BFSAgent():
    def __init__(self) -> None:
        self.env = None

    def search(self, env: DragonBallEnv) -> Tuple[List[int], float, int]:
        self.env = env
        self.env.reset()

        expanded = 0
        total_cost = 0
        actions = []
        curr_state = self.env.get_initial_state()
        num_state = curr_state[0]
        is_terminated = False
        d1_status = self.env.d1[0] == curr_state[0]
        d2_status = self.env.d2[0] == curr_state[0]
        curr_node = Node(None, num_state, actions.copy(), total_cost, is_terminated, d1_status, d2_status)
        open = [curr_node]
        close = []

        while open:
            curr_node = open.pop(0)
            close.append(curr_node)
            expanded += 1
            if self.env.is_final_state(curr_state):
                return (curr_node.c_actions, curr_node.c_total_cost, expanded-1)
            elif (curr_node.c_terminated) or (num_state == (self.env.nrow * self.env.ncol-1)):
                expanded = expanded-1
                continue
            for action, son in self.env.succ(curr_state).items():
                num_state = son[0][0]
                actions = curr_node.c_actions.copy()
                actions.append(action)
                total_cost = curr_node.c_total_cost + son[1]
                is_terminated = son[2]
                d1_status = (curr_node.c_d1_status) or (son[0][0]==self.env.d1[0])   #assert if its good or should be (son[0][1])
                d2_status = (curr_node.c_d2_status) or (son[0][0]==self.env.d2[0])
                new_state = (son[0][0], d1_status, d2_status)
                new_node = Node(None, num_state, actions.copy(), total_cost, is_terminated, d1_status, d2_status)      
                if new_node not in open and new_node not in close:
                    open.append(new_node)
        return ([], 0, 0)


""" WeightedAStarAgent"""


        

class WeightedAStarAgent():
    def __init__(self) -> None:
        self.env = None

    def hmsap(self, state: Tuple[int, bool, bool]):
        min_dist = self.env.ncol+self.env.nrow
        if (not state[1]):
            if (not state[2]):
                min_dist = min(self.menhaten_dist(state, self.env.d1), self.menhaten_dist(state, self.env.d2))
            else:
                min_dist = self.menhaten_dist(state, self.env.d1)
        elif (not state[2]):
            min_dist = self.menhaten_dist(state, self.env.d2)
        for g in self.env.get_goal_states():
            if (self.menhaten_dist(state, g)<min_dist):
                min_dist = self.menhaten_dist(state, g)
        return min_dist
    
    def menhaten_dist(self, state1: Tuple[int, bool, bool], state2: Tuple[int, bool, bool]):
        col1, row1 = self.env.to_row_col(state1)
        col2, row2 = self.env.to_row_col(state2)
        return (abs(col1-col2)+ abs(row1-row2))
    

    def search(self, env: DragonBallEnv, h_weight) -> Tuple[List[int], float, int]:
        self.env = env
        self.env.reset()

        expanded = 0
        total_cost = 0
        actions = []
        curr_state = self.env.get_initial_state()
        num_state = curr_state[0]
        is_terminated = False
        d1_status = self.env.d1[0] == curr_state[0]
        d2_status = self.env.d2[0] == curr_state[0]

        new_f = (1-h_weight)*total_cost + h_weight*self.hmsap(curr_state)
        

        open = heapdict.heapdict()
        close = heapdict.heapdict()

        open[curr_state] = Node(new_f, num_state, actions.copy(), total_cost, is_terminated, d1_status, d2_status)      #check terminated value

        while (open):       #is it correct syntax?
            curr_state, curr_node = open.popitem()      #the order relation is defined?
            close[curr_state] = curr_node
            expanded = expanded+1
            if (self.env.is_final_state(curr_state)):
                return (curr_node.c_actions, curr_node.c_total_cost, expanded-1)
            elif ((curr_node.c_terminated) or (curr_state[0] == (self.env.nrow * self.env.ncol-1))):
                expanded = expanded-1
                continue
            for action, son in self.env.succ(curr_state).items() :
               num_state = son[0][0]
               actions = curr_node.c_actions.copy()
               actions.append(action)
               total_cost = curr_node.c_total_cost + son[1]
               is_terminated = son[2]
               d1_status = (curr_node.c_d1_status) or (son[0][0]==self.env.d1[0])   #assert if its good or should be (son[0][1])
               d2_status = (curr_node.c_d2_status) or (son[0][0]==self.env.d2[0])
               new_state = (son[0][0], d1_status, d2_status)
               new_f = (1-h_weight)*(total_cost) + h_weight*self.hmsap(new_state)
               new_node = Node(new_f, num_state, actions.copy(), total_cost, is_terminated, d1_status, d2_status)       #consider remove statuses in Node

               if ((not open.get(new_state)) and (not close.get(new_state))):
                   open [new_state] = new_node
               elif (open.get(new_state)):
                   old_version = open.get(new_state)
                   if (new_node.c_f<old_version.c_f):
                       open [new_state] = new_node
               else:
                   old_version = close.get(new_state)
                   if new_node.c_f<old_version.c_f:
                       open [new_state] = new_node
                       close[new_state] = Node(-1, -1, [], -1, True, False, False)
                       close.popitem()
        
        return ([], 0, 0)


# class AStarEpsilonAgent():
#     def __init__(self) -> None:
#         raise NotImplementedError
        
#     def ssearch(self, env: DragonBallEnv, epsilon: int) -> Tuple[List[int], float, int]:
#         raise NotImplementedError
