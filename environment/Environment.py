import numpy as np
from parser import Parser
from enum import Enum

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
    
    def print_board_prettier(self):
        rows, cols = self.board.shape
        print('-' *  ((7 * self.N) + (self.N - 2))) 
        for i in range(rows):
            row_str = ''
            for j in range(cols):
                row_str += str(int(self.board[i][j])) + ' '
                if (j + 1) % 3 == 0 and j != cols - 1:
                    row_str += '| '  # Add vertical separator between 3x3 segments
            print(row_str)
            if (i + 1) % 3 == 0 and i != rows - 1:
                print('-' *  ((7 * self.N) + (self.N - 2))) 
        print('-' *  ((7 * self.N) + (self.N - 2))) 


    def move(self, src_card_num, dest_card_num):
        src_x, src_y = self.__get_coordinates_from_card_number(src_card_num)
        dest_x, dest_y = self.__get_coordinates_from_card_number(dest_card_num)
        self.board[src_x][src_y] = 1
        self.board[dest_x][dest_y] = 2
        self.robot_loc = (dest_x, dest_y)

    def shift_cards(self, axis=Axis.ROW, dir=DIRECTION.LEFTWARDS, card_row_or_col=1):
        start_idx = 3 * card_row_or_col
        try :
            if axis == Axis.ROW:
                assert not start_idx <= self.robot_loc[0] < start_idx + 3, "Moving Rows have robot! Not Allowed!"
                assert(dir == DIRECTION.LEFTWARDS or dir == DIRECTION.RIGHTWARDS)
                selected_columns = self.board[start_idx:start_idx + 3, :]
                print(selected_columns)
                shifted_columns = np.roll(selected_columns, 3 if dir == DIRECTION.RIGHTWARDS else -3, axis=axis.value)
                self.board[start_idx:start_idx + 3, :] = shifted_columns
            else:
                assert not start_idx <= self.robot_loc[1] < start_idx + 3, "Moving Columns have robot! Not Allowed!"
                assert(dir == DIRECTION.UPWARDS or dir == DIRECTION.DOWNWARDS)
                selected_columns = self.board[:, start_idx:start_idx + 3]
                shifted_columns = np.roll(selected_columns, 3 if dir == DIRECTION.DOWNWARDS else -3, axis=axis.value)
                self.board[:, start_idx:start_idx + 3] = shifted_columns
        except AssertionError as e:
            print(f"Illegal Move! : {e}")
            return False
        except Exception as e:
            print(f"General Exception : {e}")
            return False
        return True




if __name__ == "__main__":
    e = Environment(instance_file="/Users/russelltankaimin/Desktop/python_proj/project-labyrinth/7x7_instances_pddl/instance_139_7_by_7.pddl")
    e.print_board_prettier()
    e.move(0, 7)
    e.print_board_prettier()
    e.shift_cards(axis=Axis.ROW, dir=DIRECTION.RIGHTWARDS, card_row_or_col=0)
    e.print_board_prettier()
    e.shift_cards(axis=Axis.COL, dir=DIRECTION.UPWARDS, card_row_or_col=3)
    e.print_board_prettier()