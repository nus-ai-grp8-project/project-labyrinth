
from environment.Environment import Environment, Axis, DIRECTION
import random
import argparse
import os

class QLearning():
    def __init__(self, env : Environment, learning_rate = 0.8, discount_factor = 0.8, epsilon = 0.1):
        self.env = env
        self.size = env.N * 3
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.reward_move = -1
        self.reward_goal = 100
        self.q_table = dict() # state: (position, curr_env) where (curr_env) = tuple(env.board)
        self.memo = dict()
        self.directions = ((-1,0),(1,0),(0,1),(0,-1))

    def possible_adj_moves(self, row, col):
        possible_adj_pos = set()
        for direction in self.directions:
            next_row_1 = row + direction[0]
            next_col_1 = col + direction[1]
            next_row_2 = row + direction[0] * 2
            next_col_2 = col + direction[1] * 2
            # print("Check:", next_row, next_col)
            if (next_row_2 < 0 or next_row_2 >= self.size):
                continue
            if (next_col_2 < 0 or next_col_2 >= self.size):
                continue
            if (self.env.board[next_row_1, next_col_1] == 0):
                continue
            if (self.env.board[next_row_2, next_col_2] == 0):
                continue
            next_row_centre = next_row_2 + direction[0]
            next_col_centre = next_col_2 + direction[1]
            possible_adj_pos.add((next_row_centre, next_col_centre))
        return possible_adj_pos

    def possible_moves(self):
        row, col = self.env.robot_loc
        graph = self.env.board
        possible_pos = set()
        seen = set()
        stack = list()
        stack.append(self.env.robot_loc)
        while len(stack) > 0:
            next_pos = stack.pop()
            if next_pos in seen:
                continue
            possible_pos.add(next_pos)
            seen.add(next_pos)
            possible_next_positions = self.possible_adj_moves(next_pos[0], next_pos[1])
            for possible_next_position in possible_next_positions:
                if possible_next_position not in seen:
                    stack.append(possible_next_position)
        return possible_pos

    def possible_envs(self):
        curr_pos = self.env.robot_loc
        next_graphs = set()
        for i in range(self.env.N):
            for direction in DIRECTION:
                posssible_row = self.env.shift_cards(Axis.ROW, direction, i) # Shift row
                if posssible_row:
                    next_graphs.add((curr_pos, self.tuple_env(self.env.robot_loc, self.env.board))) # Add to possible next states
                    self.env.shift_cards(Axis.ROW, self.opp_direction(direction), i) # Revert shift
                    
                posssible_col = self.env.shift_cards(Axis.COL, direction, i) # Shift col
                if posssible_col:
                    next_graphs.add((curr_pos, self.tuple_env(self.env.robot_loc, self.env.board))) # Add to possible next states
                    self.env.shift_cards(Axis.COL,  self.opp_direction(direction), i) # Revert shift
        self.memo[self.tuple_env(self.env.robot_loc, self.env.board)] = next_graphs
        return next_graphs 
        
    def reward(self):
        if self.env.board[self.env.robot_loc] == 5:
            return self.reward_goal
        return self.reward_move

    def tuple_env(self, pos, env):
        return (pos, tuple(map(lambda x : tuple(x.astype(int)), env)))

    def opp_direction(self, direction):
        match direction:
            case DIRECTION.LEFTWARDS:
                return DIRECTION.RIGHTWARDS
            case DIRECTION.RIGHTWARDS:
                return DIRECTION.LEFTWARDS
            case DIRECTION.UPWARDS:
                return DIRECTION.DOWNWARDS
            case DIRECTION.DOWNWARDS:
                return DIRECTION.UPWARDS
                
    def randomly_move_board(self):
        index = random.randint(0, self.env.N - 1)
        direction = random.randint(0, 3)
        match direction:
            case 0:
                self.env.shift_cards(Axis.ROW, DIRECTION.LEFTWARDS, index)
                # print(f"Randomly moved row {index} leftwards") 
            case 1:
                self.env.shift_cards(Axis.ROW, DIRECTION.RIGHTWARDS, index)
                # print(f"Randomly moved row {index} rightwards") 
            case 2:
                self.env.shift_cards(Axis.COL, DIRECTION.UPWARDS, index)
                # print(f"Randomly moved col {index} upwards") 
            case 3:
                self.env.shift_cards(Axis.COL, DIRECTION.DOWNWARDS, index)
                # print(f"Randomly moved col {index} downwards") 

    def get_card_number_from_coordinates(self, move):
        row_index = (move[0] - 1) // 3
        col_index = (move[1] - 1) // 3
        card_number = (row_index * self.env.N) + col_index
        return card_number

    # Q Learning without filling a q table first
    def Q_learning_1(self, num_episodes=1000, f=None, verbose=False):
        self.q_table = dict()
        for episode in range(num_episodes):
            if verbose:
                print("=========================================", file=f, flush=True)
                print(f"Episode: {episode}", file=f, flush=True)
                print("Q Table:", file=f, flush=True)
                pretty_print_q_table(self.q_table, f)
            print("Episode:", episode)
            done = False
            while not done:
                tuple_curr_env = self.tuple_env(self.env.robot_loc, self.env.board)
                next_possible_moves = list(self.possible_moves())
                q_table_env = self.q_table.get(tuple_curr_env, {k: (self.reward_goal if self.env.board[k] == 5 else 0) for k in next_possible_moves}) # Get Row in Q Table
                self.q_table[tuple_curr_env] = q_table_env # Assign new dict if empty
                temp = list()
                if (random.random() < self.epsilon): # Exploration
                    temp2 = list()
                    temp2.append(random.choice(next_possible_moves))
                    next_possible_moves = temp2
                for pos_move in next_possible_moves:
                    q_table_val = q_table_env.get(pos_move, 0) # Q Value for state and move
                    next_envs = self.memo.get(tuple_curr_env, self.possible_envs())
                    q_table_val += (self.learning_rate *
                                    (self.reward() +
                                    self.discount_factor * max([max(self.q_table.get(tuple_curr_env).values()) for env in next_envs]) -
                                    q_table_val))
                    self.q_table[tuple_curr_env][pos_move] = q_table_val
                    temp.append(q_table_val)
                next_best_move = min(range(len(temp)), key=temp.__getitem__)
                if self.env.board[next_possible_moves[next_best_move]] == 5:
                    done = True
                    break
                self.env.move(self.get_card_number_from_coordinates(self.env.robot_loc),
                            self.get_card_number_from_coordinates(next_possible_moves[next_best_move]))
                self.randomly_move_board()
        return self.q_table

def print_board_prettier(board, f):
        n = len(board[0])
        print('-' *  (3 * n), file=f, flush=True) 
        for i in range(n):
            row_str = ''
            for j in range(n):
                row_str += str(int(board[i][j])) + ' '
                if (j + 1) % 3 == 0 and j != n - 1:
                    row_str += '| '  # Add vertical separator between 3x3 segments
            print(row_str, file=f, flush=True)
            if (i + 1) % 3 == 0 and i != n - 1:
                print('-' *  (3 * n), file=f, flush=True) 
        print('-' *  (3 * n), file=f, flush=True) 

def pretty_print_q_table(q_table, f):
    for k, v in q_table.items():
        print("Position:", k[0], file=f, flush=True)
        print("Board:", file=f)
        print_board_prettier(k[1], f)
        print("Q Values:", v, file=f, flush=True)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning_rate', type=float, required=True, help="Learning rate for the Q-Learning algorithm")
    parser.add_argument('--discount_factor', type=float, required=True, help="Discount factor for the Q-Learning algorithm")
    parser.add_argument('--epsilon', type=float, required=True, help="Epsilon for the Q-Learning algorithm")
    parser.add_argument('--episodes', type=int, required=True, help="Number of episodes to run the Q-Learning algorithm")
    parser.add_argument('--verbose', default=False, action='store_true')
    args = parser.parse_args()
    
    for i in range(0, 1):
        new_env = Environment(instance_file=rf"3x3_instances_pddl/instance_{i}_3_by_3.pddl")
        Q_learning = QLearning(new_env, args.learning_rate, args.discount_factor, args.epsilon)
        filepath = rf"output/lr_{args.learning_rate}_discount_{args.discount_factor}_epsilon_{args.epsilon}_episodes_{args.episodes}_instance_{i}_3_by_3.txt"
        os.makedirs("output", exist_ok=True)
        f = open(filepath, 'w+')
        q_table = Q_learning.Q_learning_1(args.episodes, f, args.verbose)
        f.close()
        filepath = rf"output/lr_{args.learning_rate}_discount_{args.discount_factor}_epsilon_{args.epsilon}_episodes_{args.episodes}_instance_{i}_3_by_3_final.txt"
        f = open(filepath, 'w+')
        pretty_print_q_table(q_table, f)
        f.close()
