from collections import deque
from enum import Enum
from config import Config


class Direction(Enum):
    UP = [0, -1]
    LEFT = [-1, 0]
    RIGHT = [1, 0]
    DOWN = [0, 1]

    DOUBLE_UP = [0, -2]
    DOUBLE_LEFT = [-2, 0]
    DOUBLE_RIGHT = [2, 0]
    DOUBLE_DOWN = [0, 2]

    UP_LEFT = [-1, -1]
    UP_RIGHT = [1, -1]
    DOWN_LEFT = [-1, 1]
    DOWN_RIGHT = [1, 1]

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Pawn:


    def __init__(self, name, position, walls):
        self.name = name
        self.color = Config.GREEN if self.name == 'Green' else Config.RED
        self.target = 0 if name == 'Green' else 8
        self.position = position
        self.walls = walls
        self.remaining_walls = 10
        self.opponent = None

    def set_opponent(self, opponent):
        self.opponent = opponent

    def closest_path_length(self):
        # Initialize BFS queue with the starting position
        start = (self.position.col, self.position.row)
        queue = deque([start])

        # Boolean map to track visited positions
        bool_map = [[False for _ in range(Config.MAP_SIZE)] for __ in range(Config.MAP_SIZE)]
        bool_map[self.position.row][self.position.col] = True

        # Dictionary to keep track of parents (for path reconstruction)
        parents = {start: None}

        while queue:
            current = queue.popleft()
            moves = self.possible_moves()

            for move in moves:
                next_pos = tuple(a + b for a, b in zip(current, move.value))

                # Ensure the move is within bounds and not visited
                if 0 <= next_pos[0] < self.MAP_SIZE and 0 <= next_pos[1] < self.MAP_SIZE:
                    if not bool_map[next_pos[1]][next_pos[0]]:
                        bool_map[next_pos[1]][next_pos[0]] = True
                        parents[next_pos] = current  # Track the parent node

                        # Check if we have reached the target
                        if next_pos == self.target:
                            return self.reconstruct_path(parents, next_pos)  # Reconstruct the path

                        queue.append(next_pos)

        return -1  # Return -1 if no path found

    def reconstruct_path(self, parents, target):
        path = []
        current = target

        # Backtrack from the target to the start using the parent references
        while current is not None:
            path.append(current)
            current = parents[current]

        # The path is constructed in reverse, so we reverse it before returning
        path.reverse()
        return len(path) - 1  # Returning the length of the path (excluding the start position)

    def move(self, moveDir):
        moveCords = moveDir.value
        self.col += moveCords[0]
        self.row += moveCords[1]

    def place_wall(self, wall_id):
        self.remaining_walls -= 1
        self.walls.append(wall_id)

    def is_target_reached(self):
        return self.position.row == self.target

    def possible_moves(self, position=None):
        """Returns the available possible moves for the
        given coordinates or current location of pawn when left blank."""

        if position is None:
            self.position = position
        moves = list()
        # --Move Checks
        # -Direction Up
        if position.row > 0 and f"ver_wall#{position.row-1}-{position.col}" in self.walls:
            # Next Cell is Empty
            if not (position.row == self.opponent.position.row and position.col - 1 == self.opponent.position.col):
                moves.append(Direction.UP)
            else:  # Next Cell Have Opponent
                if position.row - 1 > 0 and f"ver_wall#{position.row-2}-{position.col}" in self.walls:
                    moves.append(Direction.DOUBLE_UP)
                else:  # Wall Blocks Double Up
                    if position.col > 0 and f"hor_wall#{position.row-1}-{position.col-1}" in self.walls:
                        moves.append(Direction.UP_LEFT)
                    if position.col < 8 and f"hor_wall#{position.row-1}-{position.col}" in self.walls:
                        moves.append(Direction.UP_RIGHT)
        # -Direction Left
        if position.col > 0 and f"hor_wall#{position.row}-{position.col-1}" in self.walls:
            # Next Cell is Empty
            if not (position.col - 1 == self.opponent.position.col and position.row == self.opponent.position.row):
                moves.append(Direction.LEFT)
            else:  # Next Cell Have Opponent
                if position.col - 1 > 0 and f"hor_wall#{position.row}-{position.col-2}" in self.walls:
                    moves.append(Direction.DOUBLE_LEFT)
                else:  # Wall Blocks Double Left
                    if position.row > 0 and f"ver_wall#{position.row-1}-{position.col-1}" in self.walls:
                        moves.append(Direction.UP_LEFT)
                    if position.row < 8 and f"ver_wall#{position.row}-{position.col-1}" in self.walls:
                        moves.append(Direction.DOWN_LEFT)
        # -Direction Right
        if position.col < 8 and f"ver_wall#{position.row}-{position.col}" in self.walls:
            # Next Cell is Empty
            if not (position.col + 1 == self.opponent.position.col and position.row == self.opponent.position.row):
                moves.append(Direction.RIGHT)
            else:  # Next Cell Have Opponent
                if position.col + 1 < 8 and f"ver_wall#{position.row}-{position.col+1}" in self.walls:
                    moves.append(Direction.DOUBLE_RIGHT)
                else:  # Wall Blocks Double Right
                    if position.row > 0 and f"hor_wall#{position.row-1}-{position.col+1}" in self.walls:
                        moves.append(Direction.UP_RIGHT)
                    if position.row < 8 and f"ver_wall#{position.row}-{position.col+1}" in self.walls:
                        moves.append(Direction.DOWN_RIGHT)

        # -Direction Down
        if position.row < 8 and f"hor_wall#{position.row}-{position.col}" in self.walls:
            # Next Cell is Empty
            if not (position.col == self.opponent.position.col and position.row + 1 == self.opponent.position.row):
                moves.append(Direction.DOWN)
            else:  # Next Cell Have Opponent
                if position.row + 1 < 8 and f"hor_wall#{position.row+1}-{position.col}" in self.walls:
                    moves.append(Direction.DOUBLE_DOWN)
                else:  # Wall Blocks Double Down
                    if position.col > 0 and f"ver_wall#{position.row+1}-{position.col-1}" in self.walls:
                        moves.append(Direction.DOWN_LEFT)
                    if position.col < 8 and f"ver_wall#{position.row+1}-{position.col}" in self.walls:
                        moves.append(Direction.DOWN_RIGHT)
        return moves