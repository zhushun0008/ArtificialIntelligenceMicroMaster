'''
Author: zhushun0008
Email: zhushun0008@gmail.com
'''

from BaseAI import BaseAI

MAX_VALUE = 1000000
MIN_VALUE = -1000000
MAX_DEPTH = 6


class PlayerAI(BaseAI):
    def getMove(self, grid):
        (max_move, max_utility) = maximize(grid, 0)
        return max_move


def maximize(grid, current_depth):
    moves = grid.getAvailableMoves()
    if len(moves) == 0 or current_depth > MAX_DEPTH:
        return (None, grid.getMaxTile())
    (max_move, max_utility) = (None, MIN_VALUE)
    for temp_move in moves:
        gridCopy = grid.clone()
        if gridCopy.move(temp_move):
            (_, temp_utility) = minimize(gridCopy, current_depth + 1)
            if temp_utility > max_utility:
                (max_move, max_utility) = (temp_move, temp_utility)
    return (max_move, max_utility)


def minimize(grid, current_depth):
    moves = grid.getAvailableMoves()
    if len(moves) == 0 or current_depth > MAX_DEPTH:
        return (None, grid.getMaxTile())
    (min_move, min_utility) = (None, MAX_VALUE)
    for temp_move in moves:
        gridCopy = grid.clone()
        if gridCopy.move(temp_move):
            (_, temp_utility) = maximize(gridCopy, current_depth + 1)
            if temp_utility < min_utility:
                (min_move, min_utility) = (temp_move, temp_utility)
    return (min_move, min_utility)
