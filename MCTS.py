import time
import random
from math import *
from copy import *
from StarBattle import *
import sys, os

class Node():
    
    def __init__(self, parent, state: Decision):
        self.total_simulations = 0
        self.score = 0
        self.children = []
        self.parent = parent
        self.state = state
        self.terminal = False
        self.numExpand = 0
        
    def expand(self, board: Board):
        #print(f'Begin expansion, current: {self.state.decisions}')
        sys.stdout = open(os.devnull, 'w')
        valid = self.state.valid_point(board)
        sys.stdout = sys.__stdout__
        self.numExpand += 1
        #print(f'valid: {valid}')
        if not valid:
            #self.backprop(self.state.score()[0])
            self.score = -10000000000
            self.terminal = True
            parent = self.parent
            while parent.isTerminal():
                parent.score = -10000000000
                parent = parent.parent
        for i,j in valid:
            child_state = deepcopy(self.state)
            child_state.move(i,j)
            child_node = Node(self, child_state)
            self.children.append(child_node)
    
    def isTerminal(self):
        terminal = True
        for i in self.children:
            if not i.terminal:
                return False
        self.terminal = terminal
        return terminal

    def backprop(self, reward):
        self.total_simulations += 1
        self.score += reward
        if self.parent != None: # Only do for non-root nodes
            self.parent.backprop(reward)
    
    def exploration_term(self):
        return sqrt(log(self.parent.total_simulations)/max(self.total_simulations, 0.01))
    
    def exploitation_term(self):
        #return 0
        return self.score/max(self.total_simulations, 0.01)

class MCTS():
    def __init__(self, exploration_parameter=sqrt(2), time_limit=None):
        self.exploration_parameter = exploration_parameter
        self.time_limit = time_limit
        self.num_node = 0
        self.node_solved = 0
        # TODO Check time_limit is not None
    
    def simulate(self, decision: Decision, board: Board):
        #print(f'Begin simulation')
        valid = decision.valid_point(board)
        while valid:
            random_index = random.randint(0,len(valid)-1)
            i = valid[random_index][0]
            j = valid[random_index][1]
            decision.move(i,j)
            valid = decision.valid_point(board)
        score = decision.score()
        return score
    
    def select(self, node):
        # TODO REWRITE
        if not node.children: # Not expanded
            return node
        
        sorted_children = sorted(node.children, key=lambda child : child.exploitation_term() + self.exploration_parameter*child.exploration_term(), reverse=True)
        positive = [i for i in sorted_children if i.score >= 0]
        if not positive:
            return None
        return self.select(sorted_children[0])
    
    def play(self, init_state: Decision, board: Board):
        root = Node(None, init_state)
        self.num_node += 1
        max_score = board.star*board.shape
        best_score = 0
        start = time.time()
        while time.time() - start < self.time_limit:
            selected_node = self.select(root)
            # DELETE
            print("Best score: ", best_score, "   max score:", max_score)
            # DELETE
            if selected_node.total_simulations == 0:
                score, solution = self.simulate(deepcopy(selected_node.state), board)
                best_score = max(best_score, score)
                if score >= max_score:
                    print("SOLVED")
                    print(f'Solution is {solution}')
                    return
                selected_node.backprop(score/max_score)
            else:
                if selected_node.numExpand >= 2:
                    print(f'WARNING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                selected_node.expand(board)
                