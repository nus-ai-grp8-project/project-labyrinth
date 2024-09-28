import numpy as np
from parser import Parser
from enum import Enum
from collections import deque

class Axis(Enum):
    ROW = 1
    COL = 0

class DIRECTION(Enum):
    LEFTWARDS = 0
    RIGHTWARDS = 1
    UPWARDS = 2
    DOWNWARDS = 3


class Environment:
    """
    The board, its representations and its actions
    """

    def __init__(self, instance_file : str = ""):
        self.instance_file = instance_file
        self.parser = Parser()
        self.board: np.ndarray = self.parser.get_board(instance_file)
        self.N = self.board.shape[0] // 3
        print(f"Environment and {self.N}x{self.N} Board initialised !\n")
        self.__set_object_state_on_board()
        self.robot_loc = (1, 1)
        # print(f"Board: \n{self.board}")

    def __set_object_state_on_board(self):
        x = (self.N - 1) * 3 + 1
        y = x
        self.board[x][y] = 5
        print("Goal Set! Represented as 5")
        self.board[1][1] = 2
        print("Robot Set! Represented as 2")

    def __get_coordinates_from_card_number(self, card_number):
        row = (card_number // self.N) * 3 + 1
        col = (card_number % self.N) * 3 + 1
        return (row, col)
    
    def __get_card_number_from_coordinates(self, row, col):
        return (row // 3) * self.N + (col // 3)
    
    def __get_card_coordinates_from_card_number(self, card_number):
        x, y = self.__get_coordinates_from_card_number(card_number)
        row = x // 3
        col = y // 3
        return (row, col)
    
    def is_valid_move(self, src_card_num, dest_card_num):
        src_x, src_y = self.__get_coordinates_from_card_number(src_card_num)
        dest_x, dest_y = self.__get_coordinates_from_card_number(dest_card_num)

        # Check if source and destination are within the board
        if src_x < 0 or src_x >= self.board.shape[0] or src_y < 0 or src_y >= self.board.shape[1]:
            print("Invalid move: Source is out of bounds!")
            return False
        
        if dest_x < 0 or dest_x >= self.board.shape[0] or dest_y < 0 or dest_y >= self.board.shape[1]:
            print("Invalid move: Destination is out of bounds!")
            return False

        
        # Check for walls between source and destination cards
        if src_x == dest_x:  # Moving horizontally
            if src_y < dest_y:  # Moving right
                if self.board[src_x][src_y + 1] == 0 or self.board[dest_x][dest_y - 1] == 0:  # Check right border of source card
                    print("Invalid move: Wall blocks movement to the right!")
                    return False
            elif src_y > dest_y:  # Moving left
                if self.board[src_x][src_y - 1] == 0 or self.board[dest_x][dest_y + 1] == 0:  # Check left border of source card
                    print("Invalid move: Wall blocks movement to the left!")
                    return False

        elif src_y == dest_y:  # Moving vertically
            if src_x < dest_x:  # Moving down
                if self.board[src_x + 1][src_y] == 0 or self.board[dest_x - 1][dest_y] == 0:  # Check bottom border of source card
                    print("Invalid move: Wall blocks movement down!")
                    return False
            elif src_x > dest_x:  # Moving up
                if self.board[src_x - 1][src_y] == 0 or self.board[dest_x + 1][dest_y] == 0:  # Check top border of source card
                    print("Invalid move: Wall blocks movement up!")
                    return False
        
        # Check if the destination is adjacent to the source (only horizontal or vertical moves allowed)
        if not ((abs(dest_x - src_x) == 3 and dest_y == src_y) or (abs(dest_y - src_y) == 3 and dest_x == src_x)):
            print("Invalid move: The destination is not adjacent to the source!")
            return False

        return True
        
    def is_path_exist(self, src_card_num, dest_card_num):
        rows, cols = self.board.shape
        src_x, src_y = self.__get_coordinates_from_card_number(src_card_num)
        dest_x, dest_y = self.__get_coordinates_from_card_number(dest_card_num)
        src = (src_x, src_y)
        dest = (dest_x, dest_y) 

        visited = np.zeros((rows, cols), dtype=bool)
        queue = deque([src])

        # All possible directions: left, right, up, down
        directions = [("right", (0, 3)), ("left", (0, -3)), ("down", (3, 0)), ("up", (-3, 0))]


        while queue:
            x, y = queue.popleft()
            if (x, y) == dest:
                return True
            
            visited[x][y] = True

            # Explore all four directions
            for direction_name, (dx, dy) in directions:
                nx, ny = x + dx, y + dy
                src_card_num = self.__get_card_number_from_coordinates(x, y)
                dest_card_num = self.__get_card_number_from_coordinates(nx, ny)
                if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and self.is_valid_move(src_card_num, dest_card_num):
                    src_card_coordinates = self.__get_card_coordinates_from_card_number(src_card_num)
                    dest_card_coordinates = self.__get_card_coordinates_from_card_number(dest_card_num)
                    print(f"Moving from {src_card_coordinates} in {direction_name} to {dest_card_coordinates}")
                    
                    queue.append((nx, ny))


        return False




    def print_board_prettier(self):
        rows, cols = self.board.shape
        wall_char = '#'  # Represent blocked walls
        path_char = ' '  # Represent open paths
        robot_char = 'R'  # Represent the robot
        goal_char = 'G'   # Represent the goal

        print('-' * ((7 * self.N) + (self.N - 2)))  # Top border of the maze
        for i in range(rows):
            row_str = ''
            for j in range(cols):
                if self.board[i][j] == 0:
                    row_str += wall_char + ' '  
                elif self.board[i][j] == 1:
                    row_str += path_char + ' '  
                elif self.board[i][j] == 2:
                    row_str += robot_char + ' '  
                elif self.board[i][j] == 5:
                    row_str += goal_char + ' '  

                if (j + 1) % 3 == 0 and j != cols - 1:
                    row_str += '| '  # Vertical separators between 3x3 segments

            print(row_str)
            if (i + 1) % 3 == 0 and i != rows - 1:
                print('-' * ((7 * self.N) + (self.N - 2)))  # Horizontal separators between 3x3 segments
        print('-' * ((7 * self.N) + (self.N - 2)))  # Bottom border of the maze

    def move(self, src_card_num, dest_card_num):
        if self.is_path_exist(src_card_num, dest_card_num):
            print("Path Exists!")
            src_x, src_y = self.__get_coordinates_from_card_number(src_card_num)
            dest_x, dest_y = self.__get_coordinates_from_card_number(dest_card_num)
            self.board[src_x][src_y] = 1
            self.board[dest_x][dest_y] = 2
            self.robot_loc = (dest_x, dest_y)

            src_card_coordinates = self.__get_card_coordinates_from_card_number(src_card_num)
            dest_card_coordinates = self.__get_card_coordinates_from_card_number(dest_card_num)
            print(f"Moved from {src_card_coordinates} to {dest_card_coordinates} successfully!")
        else:
            print("Path does not exist!")
            

    def shift_cards(self, axis=Axis.ROW, dir=DIRECTION.LEFTWARDS, card_row_or_col=1):
        start_idx = 3 * card_row_or_col
        try :
            if axis == Axis.ROW:
                assert not start_idx <= self.robot_loc[0] < start_idx + 3, "Moving Rows have robot! Not Allowed!"
                assert(dir == DIRECTION.LEFTWARDS or dir == DIRECTION.RIGHTWARDS)
                selected_columns = self.board[start_idx:start_idx + 3, :]
                # print("Before Shift selected column/row")
                print(selected_columns)
                shifted_columns = np.roll(selected_columns, 3 if dir == DIRECTION.RIGHTWARDS else -3, axis=axis.value)
                self.board[start_idx:start_idx + 3, :] = shifted_columns
                print(f"Shifting Row {card_row_or_col} {dir}")
            else:
                assert not start_idx <= self.robot_loc[1] < start_idx + 3, "Moving Columns have robot! Not Allowed!"
                assert(dir == DIRECTION.UPWARDS or dir == DIRECTION.DOWNWARDS)
                selected_columns = self.board[:, start_idx:start_idx + 3]
                shifted_columns = np.roll(selected_columns, 3 if dir == DIRECTION.DOWNWARDS else -3, axis=axis.value)
                self.board[:, start_idx:
                start_idx + 3] = shifted_columns
                print(f"Shifting Column {card_row_or_col} {dir}")
        except AssertionError as e:
            print(f"Illegal Move! : {e}")
            return False
        except Exception as e:
            print(f"General Exception : {e}")
            return False
        return True




if __name__ == "__main__":
    e = Environment(instance_file="/Users/dunliang/Downloads/cs4246-labyrinth/5x5_instances_pddl/instance_4_5_by_5.pddl")
    e.print_board_prettier()
    e.move(0, 2)
    e.print_board_prettier()
    # e.shift_cards(axis=Axis.ROW, dir=DIRECTION.RIGHTWARDS, card_row_or_col=1)
    
    # e.print_board_prettier(step=2)
    # e.shift_cards(axis=Axis.COL, dir=DIRECTION.UPWARDS, card_row_or_col=3)
    e.move(2, 15)
    e.print_board_prettier()