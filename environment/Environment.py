import numpy as np
from environment.parser import Parser
from enum import Enum
from copy import deepcopy
import random
from collections import deque

DEBUG = False

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
        print(f"Environment and {self.N}x{self.N} Board initialised !\n") if DEBUG else None
        self.__set_object_state_on_board()
        self.robot_loc = (1, 1)
        # print(f"Board: \n{self.board}")

    def reset(self):
        self.board = self.parser.get_board(self.instance_file)
        self.__set_object_state_on_board()
        self.robot_loc = (1,1)
        print("Environment State has reset!") if DEBUG else None
        state = np.array(self.board)
        state = state.flatten()
        return state

    def print_grid_with_edges(self):
        n = self.N
        adjacency_list = self.build_card_graph()
        # Grid with n x n nodes
        for i in range(n):
            # Print the current row (node values and horizontal connections)
            for j in range(n):
                node = i * n + j  # Calculate node number based on row and column
                
                # Print the current node
                print(f"{node:2}", end="")

                # Check if there is a horizontal edge (right neighbor)
                if j < n - 1:  # Not the last column
                    right_node = node + 1
                    if right_node in adjacency_list[node]:
                        print(" —", end="")  # Horizontal edge
                    else:
                        print("  ", end="")  # No edge
            print()  # Move to the next line

            # Print vertical connections (between current and next row), except after the last row
            if i < n - 1:
                for j in range(n):
                    node = i * n + j
                    down_node = node + n  # Calculate the node below
                    if down_node in adjacency_list[node]:
                        print(" |  ", end="")  # Vertical edge
                    else:
                        print("    ", end="")  # No edge
                print()  # Move to the next line



    # def build_card_graph(self):
    #     board = deepcopy(self.board)
    #     adj_list = {
    #         i : set() for i in range(self.N * self.N)
    #     }
    #     for i in range(self.N * self.N):
    #         row, col = self.__get_coordinates_from_card_number(i)
    #         top = (row - 1, col)
    #         bottom = (row + 1, col)
    #         left = (row, col - 1)
    #         right = (row, col + 1)
    #         print(f"Testing on Card {i}") if DEBUG else None
    #         # Test TOP
    #         if 0 <= top[0] < self.N * 3 and 0 <= top[1] < self.N * 3 and board[top[0], top[1]] == 1:
    #             if 0 <= i - self.N < self.N * self.N:
    #                 row_, col_ = self.__get_coordinates_from_card_number(i - self.N)
    #                 if board[row_ + 1, col_] == 1:
    #                     adj_list[i].add(i - self.N)
                        
            
    #         # Test BOTTOM
    #         if 0 <= bottom[0] < self.N * 3 and 0 <= bottom[1] < self.N * 3 and board[bottom[0], bottom[1]] == 1:
    #             if 0 <=  i + self.N < self.N * self.N:
    #                 row_, col_ = self.__get_coordinates_from_card_number(i + self.N)
    #                 print(f"Bottom coords : {bottom}") if DEBUG else None
    #                 print(f"Bottom Card Top coords: {row_-1, col_}") if DEBUG else None
    #                 if board[row_ - 1, col_] == 1:
    #                     adj_list[i].add(i + self.N)
    #                     print(f"{i} - {i + self.N}") if DEBUG else None

    #         # Test LEFT
    #         if 0 <= left[0] < self.N * 3 and 0 <= left[1] < self.N * 3 and board[left[0], left[1]] == 1:
    #             if 0 <= i - 1 < self.N * self.N:
    #                 row_, col_ = self.__get_coordinates_from_card_number(i - 1)
    #                 if board[row_, col_ + 1] == 1:
    #                     adj_list[i].add(i - 1)
            
    #         # Test RIGHT
    #         if 0 <= right[0] < self.N * 3 and 0 <= right[1] < self.N * 3 and board[right[0], right[1]] == 1:
    #             if 0 <= i + 1 < self.N * self.N:
    #                 row_, col_ = self.__get_coordinates_from_card_number(i + 1)
    #                 if board[row_, col_ - 1] == 1:
    #                     adj_list[i].add(i + 1)
            
    #     return adj_list 

    def build_card_graph(self):
        board = deepcopy(self.board)
        adj_list = {
            i : set() for i in range(self.N * self.N)
        }
        for i in range(self.N * self.N):
            row, col = self.__get_coordinates_from_card_number(i)
            top = (row - 1, col)
            bottom = (row + 1, col)
            left = (row, col - 1)
            right = (row, col + 1)
            print(f"Testing on Card {i}") if DEBUG else None
            # Test TOP
            if 0 <= top[0] < self.N * 3 and 0 <= top[1] < self.N * 3 and board[top[0], top[1]] == 1:
                if 0 <= i - self.N < self.N * self.N:
                    row_, col_ = self.__get_coordinates_from_card_number(i - self.N)
                    if board[row_ + 1, col_] == 1:
                        adj_list[i].add(i - self.N)
                        print("Top") if DEBUG else None
                        print(f"{i} - {i - self.N}") if DEBUG else None
                        
            
            # Test BOTTOM
            if 0 <= bottom[0] < self.N * 3 and 0 <= bottom[1] < self.N * 3 and board[bottom[0], bottom[1]] == 1:
                if 0 <=  i + self.N < self.N * self.N:
                    row_, col_ = self.__get_coordinates_from_card_number(i + self.N)
                    # print(f"Bottom coords : {bottom}") if DEBUG else None
                    # print(f"Bottom Card Top coords: {row_-1, col_}") if DEBUG else None
                    if board[row_ - 1, col_] == 1:
                        adj_list[i].add(i + self.N)
                        print("Bottom") if DEBUG else None
                        print(f"{i} - {i + self.N}") if DEBUG else None

            # Test LEFT
            if 0 <= left[0] < self.N * 3 and 0 <= left[1] < self.N * 3 and board[left[0], left[1]] == 1:
                if 0 <= i - 1 < self.N * self.N:
                    row_, col_ = self.__get_coordinates_from_card_number(i - 1)
                    if board[row_, col_ + 1] == 1:
                        adj_list[i].add(i - 1)
                        print("Left") if DEBUG else None
                        print(f"{i} - {i - 1}") if DEBUG else None
            
            # Test RIGHT
            if 0 <= right[0] < self.N * 3 and 0 <= right[1] < self.N * 3 and board[right[0], right[1]] == 1:
                if 0 <= i + 1 < self.N * self.N:
                    row_, col_ = self.__get_coordinates_from_card_number(i + 1)
                    # print(f"Right coords : {right}") if DEBUG else None
                    # print(f"Right Card Left coords: {row_, col_ - 1}") if DEBUG else None
                    if board[row_, col_ - 1] == 1:
                        adj_list[i].add(i + 1)
                        print("Right") if DEBUG else None
                        print(f"{i} - {i + 1}") if DEBUG else None
            
        print(adj_list) if DEBUG else None
        return adj_list 


    def step(self, action):

        # # Step 1 : Board moves first
        # TO_SHIFT = 1
        # shifted = 0
        # while shifted < TO_SHIFT:
        #     # pick row or col to shift
        #     random_axis = random.choice([Axis.ROW, Axis.COL]) # 0 for ROW, 1 for COL
        #     random_idx = random.choice([i for i in range(self.N)]) # Row or col index of card
        #     random_dir = random.choice([DIRECTION.LEFTWARDS, DIRECTION.RIGHTWARDS] if random_axis == Axis.ROW else [DIRECTION.UPWARDS, DIRECTION.DOWNWARDS]) # 2 for left (up) 3 for right (down)
        #     if self.shift_cards(axis=random_axis, dir=random_dir, card_row_or_col=random_idx):
        #         shifted += 1
        #         print("Shifted!") if DEBUG else None
        # print("Shifted Twice Successfully!") if DEBUG else None
        # Intermission: Build state_action_graph
        

        # if not self.shift_cards(axis=axis, dir=shift_dir, card_row_or_col=shift_index):
        #     print("Illegal Shift!") if DEBUG else None
        #     return None, -1, False  # Handle illegal shift
        
        adj_list = self.build_card_graph()
        # Step 2 : Move Robot
        robot_card_row = self.robot_loc[0] // 3
        robot_card_col = self.robot_loc[1] // 3
        robot_card_num = self.N * robot_card_row  + robot_card_col
        accessible_cards = adj_list[robot_card_num]
        

        move_action = action
        
        print("Move action:", move_action) if DEBUG else None
        match move_action:
            case DIRECTION.LEFTWARDS: 

                
                if robot_card_num % self.N == 0:
                    print("Nothing to move left on!") if DEBUG else None
                else:
                    card_dest = robot_card_num - 1
                    if card_dest in accessible_cards:
                        
                        dest_loc = self.__get_coordinates_from_card_number(card_dest)
                        self.move(self.robot_loc, dest_loc)
                        print("Moving Left!") if DEBUG else None
                    else:
                        print("Don't move!") if DEBUG else None
            case DIRECTION.RIGHTWARDS:
                
                if robot_card_num % self.N == self.N - 1:
                    print("Nothing to move right on!") if DEBUG else None
                else:
                    
                    card_dest = robot_card_num + 1
                    if card_dest in accessible_cards:
                        dest_loc = self.__get_coordinates_from_card_number(card_dest)
                        self.move(self.robot_loc, dest_loc)
                        print("Moving Right!") if DEBUG else None
                    else:
                        print("Don't move!") if DEBUG else None
            
            case DIRECTION.UPWARDS: # UP
                
                if 0 <= robot_card_num < self.N:
                    print("Nothing to move up on!") if DEBUG else None
                else:
                    card_dest = robot_card_num - self.N
                    if card_dest in accessible_cards:
                        
                        dest_loc = self.__get_coordinates_from_card_number(card_dest)
                        print(self.robot_loc, dest_loc) if DEBUG else None
                        self.move(self.robot_loc, dest_loc)
                        print("Moving Up!") if DEBUG else None 
                        # self.move(robot_card_num, card_dest)
                
                    else:
                        print("Don't move!") if DEBUG else None
            case DIRECTION.DOWNWARDS: # DOWN
                
                if self.N * self.N - self.N <= robot_card_num < self.N * self.N:
                    print("Nothing to move down on!") if DEBUG else None
                else:
                    card_dest = robot_card_num + self.N
                    if card_dest in accessible_cards:
                        
                        dest_loc = self.__get_coordinates_from_card_number(card_dest)
                        self.move(self.robot_loc, dest_loc)
                        print("Moving Down!") if DEBUG else None
                    else:
                        print("Don't move!") if DEBUG else None
            
            case _:
                print(f"Action {action} not found")
                print("Error! Invalid Action!") if DEBUG else None
                return None, -10, False

        state = np.array(self.board)
        state = state.flatten()
        # Step 3 : Calculate Reward
        # BFS to find shortest path to the goal 1.) If found, then 1/(L_2 distance), else -1
         # Step 4 : Check if its terminal
        row_g, col_g, is_terminal = self.locate_goal_check_terminal()
        print("Is Terminal State:", is_terminal) if DEBUG else None
        if is_terminal:
            print("Goal Reached!") if DEBUG else None
            return state, 1, is_terminal
        else:
            goal_card_row = row_g // 3
            goal_card_col = col_g // 3
            goal_card_num = self.N * goal_card_row  + goal_card_col
            _ , reward = self.bfs_to_goal(robot_card_num, goal_card_num)
            print(f"Reward: {reward}") if DEBUG else None
            return state, reward, is_terminal
       

    # def bfs_to_goal(self, robot_card_num, goal_card_num):
    #     adj_list = self.build_card_graph()
    #     visited = [False for _ in range(self.N * self.N)]
    #     fifo_q = deque()
    #     fifo_q.append(robot_card_num)
    #     cost = 0
    #     while fifo_q:
    #         curr = fifo_q.popleft()
    #         visited[curr] = True
    #         if curr == goal_card_num:
    #             return cost, 1
    #         neighbours = adj_list[curr]
    #         for n in neighbours:
    #             if not visited[n]:
    #                 fifo_q.append(n)
    #         cost += 1
    #     return cost, -1
    def bfs_to_goal(self, robot_card_num, goal_card_num):
        adj_list = self.build_card_graph()
        visited = [False for _ in range(self.N * self.N)]
        fifo_q = deque()
        fifo_q.append((robot_card_num, 0))  # Include depth in the queue
        while fifo_q:
            curr, depth = fifo_q.popleft()
            if visited[curr]:
                continue
            visited[curr] = True
            if curr == goal_card_num:
                return depth, 1  # High reward for reaching the goal
            neighbours = adj_list[curr]
            for n in neighbours:
                if not visited[n]:
                    fifo_q.append((n, depth + 1))
        # If goal not reachable, return negative reward based on estimated distance
        estimated_distance = self.estimate_distance(robot_card_num, goal_card_num)
        return estimated_distance, -estimated_distance
            
    def estimate_distance(self, robot_card_num, goal_card_num):
        robot_row, robot_col = divmod(robot_card_num, self.N)
        goal_row, goal_col = divmod(goal_card_num, self.N)
        return abs(robot_row - goal_row) + abs(robot_col - goal_col)


    def __set_object_state_on_board(self):
        x = (self.N - 1) * 3 + 1
        y = x
        self.board[x][y] = 5
        self.goal_loc = (x, y)
        print("Goal Set! Represented as 5") if DEBUG else None
        self.board[1][1] = 2
        self.robot_loc = (1, 1)
        print("Robot Set! Represented as 2") if DEBUG else None

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
            row_str = row_str.replace("1", " ")
            row_str = row_str.replace("0", "#")
            row_str = row_str.replace("2", "R")
            row_str = row_str.replace("5", "G")
            row_str = row_str.replace("7", "W") # Means Robot reached Goal, robot wins
            print(row_str)
            if (i + 1) % 3 == 0 and i != rows - 1:
                print('-' *  ((7 * self.N) + (self.N - 2))) 
        print('-' *  ((7 * self.N) + (self.N - 2))) 

    

    def locate_goal_check_terminal(self):
        if self.robot_loc == self.goal_loc:
            return self.goal_loc[0], self.goal_loc[1], True  # Goal reached
        else:
            return self.goal_loc[0], self.goal_loc[1], False
 
    # def locate_goal_check_terminal(self):
    #     row = 0
    #     col = 0
    #     for i in range(len(self.board)):
    #         if 5 in self.board[i]:
    #             row = i
    #             col = np.where(self.board[i] == 5)[0][0]
    #             return row, col, False
    #     return self.robot_loc[0], self.robot_loc[1], True # Robot at Goal already

    # def move(self, src_loc, dest_loc):
    #     src_x, src_y = src_loc
    #     dest_x, dest_y = dest_loc
        
    #     # Restore the source cell
    #     if self.board[src_x][src_y] == 2:
    #         self.board[src_x][src_y] = 1
    #     elif self.board[src_x][src_y] == 7:
    #         self.board[src_x][src_y] = 5  # Robot was on the goal

    #     # Update the destination cell
    #     if self.board[dest_x][dest_y] == 5:
    #         self.board[dest_x][dest_y] = 7  # Robot on the goal
    #     else:
    #         self.board[dest_x][dest_y] = 2
    #     self.robot_loc = (dest_x, dest_y)
    #     self.print_board_prettier()
    def move(self, src_loc, dest_loc):
        src_x, src_y = src_loc
        dest_x, dest_y = dest_loc
        self.board[src_x][src_y] = 1
        self.board[dest_x][dest_y] = 2
        self.robot_loc = (dest_x, dest_y)
        print("Move from ", src_loc, " to ", dest_loc) if DEBUG else None
        # self.print_board_prettier()
    # def move(self, src_card_num, dest_card_num):
    #     src_x, src_y = self.__get_coordinates_from_card_number(src_card_num)
    #     dest_x, dest_y = self.__get_coordinates_from_card_number(dest_card_num)
    #     self.board[src_x][src_y] = 1
    #     self.board[dest_x][dest_y] = 2
    #     self.robot_loc = (dest_x, dest_y)

    def shift_cards(self, axis=Axis.ROW, dir=DIRECTION.LEFTWARDS, card_row_or_col=1):
        start_idx = 3 * card_row_or_col
        try :
            if axis == Axis.ROW:
                assert not start_idx <= self.robot_loc[0] < start_idx + 3, "Moving Rows have robot! Not Allowed!"
                assert(dir == DIRECTION.LEFTWARDS or dir == DIRECTION.RIGHTWARDS)
                selected_columns = self.board[start_idx:start_idx + 3, :]
                print(selected_columns) if DEBUG else None
                shifted_columns = np.roll(selected_columns, 3 if dir == DIRECTION.RIGHTWARDS else -3, axis=axis.value)
                self.board[start_idx:start_idx + 3, :] = shifted_columns
            else:
                assert not start_idx <= self.robot_loc[1] < start_idx + 3, "Moving Columns have robot! Not Allowed!"
                assert(dir == DIRECTION.UPWARDS or dir == DIRECTION.DOWNWARDS)
                selected_columns = self.board[:, start_idx:start_idx + 3]
                shifted_columns = np.roll(selected_columns, 3 if dir == DIRECTION.DOWNWARDS else -3, axis=axis.value)
                self.board[:, start_idx:start_idx + 3] = shifted_columns
        except AssertionError as e:
            print(f"Illegal Move! : {e}") if DEBUG else None
            return False
        except Exception as e:
            print(f"General Exception : {e}")
            return False
        return True




# if __name__ == "__main__":
    # e = Environment(instance_file="/Users/dunliang/Downloads/cs4246-labyrinth/3x3_instances_pddl/instance_0_3_by_3.pddl")
    # e.print_board_prettier()
    # e.move(0, 7)
    # e.print_board_prettier()
    # e.shift_cards(axis=Axis.ROW, dir=DIRECTION.RIGHTWARDS, card_row_or_col=0)
    # e.print_board_prettier()
    # e.shift_cards(axis=Axis.COL, dir=DIRECTION.UPWARDS, card_row_or_col=3)
    # e.print_board_prettier()