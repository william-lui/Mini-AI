from __future__ import absolute_import, division, print_function
import copy
import random
from game import Game
from sys import maxsize

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree.

class Node:
    # Recommended: do not modifying this __init__ function
    def __init__(self, state, current_depth, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.depth = current_depth
        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return len(self.children) == 0
        # AI agent. To be used do determine a promising next move.


class AI:
    # Recommended: do not modifying this __init__ function
    def __init__(self, root_state, depth):
        self.root = Node(root_state, 0, MAX_PLAYER)
        self.depth = depth
        self.simulator = Game()
        self.simulator.board_size = len(root_state[0])

    # recursive function to build a game tree
    def build_tree(self, node=None):
        if node == None:
            node = self.root

        if node.depth == self.depth:
            return

        if node.player_type == MAX_PLAYER:

            for action in MOVES:
                self.simulator.reset(node.state[0], node.state[1])
                if self.simulator.move(action):
                    child = Node(self.simulator.get_state(),
                                 node.depth+1, CHANCE_PLAYER)
                    node.children.append((action, child))

        elif node.player_type == CHANCE_PLAYER:

            self.simulator.reset(node.state[0], node.state[1])
            open_tile = self.simulator.get_open_tiles()
            for i, j in open_tile:
                child = Node(self.simulator.get_state(),
                             node.depth+1, MAX_PLAYER)
                (child.state[0])[i][j] = 2
                node.children.append((None, child))

        for branch in node.children:
            self.build_tree(branch[1])

    # expectimax implementation;
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node=None):
        if node == None:
            node = self.root

        if node.is_terminal():
            return (None, node.state[1])

        elif node.player_type == MAX_PLAYER:

            value = -maxsize
            best_action = None
            for a, n in node.children:
                _, exp_val = self.expectimax(n)
                if exp_val > value:
                    best_action = a
                    value = exp_val
            return (best_action, value)

        elif node.player_type == CHANCE_PLAYER:

            value = 0
            for a, n in node.children:
                _, exp_val = self.expectimax(n)
                value += (exp_val * (1 / len(node.children)))
            return (None, value)

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    def compute_decision_ec(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction
