import random
from environment.Environment import Environment, Axis, DIRECTION
import numpy as np
import math
import copy

class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0
        self.action = action 

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_possible_actions())
        # return len(self.children) == 0
    
    # def best_child(self, exploration_weight=1.4):
    #     if len(self.children) == 0:
    #         raise ValueError("No children found to select the best child from.")
    #     choices_weights = [
    #         (child.reward / (child.visits+ 1e-6)) + exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
    #         for child in self.children
    #     ]
    #     return self.children[np.argmax(choices_weights)]
    
    def best_child(self, exploration_weight=1.4):
        if len(self.children) == 0:
            raise ValueError("No children found to select the best child from.")
        
        # Calculate UCT values with a heuristic component to prefer states closer to the goal
        choices_weights = []
        for child in self.children:
            distance_to_goal = abs(child.state.robot_loc[0] - child.state.goal_loc[0]) + abs(child.state.robot_loc[1] - child.state.goal_loc[1])
            heuristic = 1 / (1 + distance_to_goal)  # Prefer states closer to the goal
            
            # Standard UCT calculation with additional heuristic
            uct_value = (
                (child.reward / (child.visits + 1e-6)) +
                exploration_weight * math.sqrt(math.log(child.visits + 1) / (child.visits + 1e-6)) +
                0.5 * heuristic  # Weight for the heuristic
            )
            choices_weights.append(uct_value)

        return self.children[np.argmax(choices_weights)]

    def get_best_child(self):
        return self.best_child(exploration_weight=0.7)
    
    def expand(self):
        possible_actions = self.state.get_possible_actions()
        for action in possible_actions:
            if not any(child.action == action for child in self.children):
                next_state = self.state.take_action(action)
                if next_state is None:
                    continue  # Skip illegal actions
                new_node = MCTSNode(next_state, parent=self, action=action)
                self.children.append(new_node)
                return new_node
        return None

    
    def backpropagate(self, reward):
        self.visits += 1
        self.reward += reward
        current_card_number = self.state.get_current_card()
        print(f"Backpropagating - Node reward: {self.reward}, Visits: {self.visits}, Current State: {current_card_number}")
        if self.parent:
            self.parent.backpropagate(reward)

class MCTSAgent:
    def __init__(self, environment, num_simulations=10):
        self.environment = environment
        self.num_simulations = num_simulations

    def search(self, initial_state):
        root = MCTSNode(initial_state)
        
        for _ in range(self.num_simulations):
            node = self.tree_policy(root)
            if node is None:
                continue  # Skip if no node was expanded
            reward = self.rollout(node.state)
            node.backpropagate(reward)
    
        return root.best_child(exploration_weight=1.4)

        
    
    def tree_policy(self, node):
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            else:
                node = node.get_best_child()
        return node
    
    # def rollout(self, state, max_depth=50):
    #     current_state = state
    #     depth = 0
    #     # print("--------------------")
    #     # print("Current State: ", current_state.robot_loc, current_state.goal_loc)
    #     while not current_state.is_terminal() and depth < max_depth:
    #         print("Current Depth: ", depth)
    #         possible_actions = current_state.get_possible_actions()
    #         print("Possible actions: ", possible_actions)
    #         if not possible_actions:
    #             break
    #         action = random.choice(possible_actions)
    #         current_state = current_state.take_action(action)
    #         depth += 1
    #         print("Actions taken during rollout: ", action)
    #     return current_state.get_reward()
    # def rollout(self, state, max_depth=10):
    #     current_state = state
    #     depth = 0
    #     total_reward = 0
    #     while not current_state.is_terminal() and depth < max_depth:
    #         possible_actions = current_state.get_possible_actions()
    #         if not possible_actions:
    #             break
    #         action = random.choice(possible_actions)
    #         next_state = current_state.take_action(action)
    #         if next_state is None:
    #             # Skip illegal actions
    #             continue
    #         total_reward += next_state.get_reward()
    #         current_state = next_state
    #         depth += 1
    #     return total_reward


    def rollout(self, state, max_depth=10):
        current_state = state
        depth = 0
        total_reward = 0
        while not current_state.is_terminal() and depth < max_depth:
            possible_actions = current_state.get_possible_actions()
            if not possible_actions:
                break
            
            # Introduce a heuristic to prefer moves that minimize distance to goal
            action = self.rollout_policy(possible_actions)
            next_state = current_state.take_action(action)
            if next_state is None:
                continue
            total_reward += next_state.get_reward()
            current_state = next_state
            depth += 1
        return total_reward
    
    def rollout_policy(self, possible_actions):
        return possible_actions[np.random.randint(len(possible_actions))]

    # def choose_action_towards_goal(self, state, possible_actions):
    #     # Use Manhattan distance or any other heuristic to pick action closer to the goal
    #     best_action = None
    #     min_distance = float('inf')
    #     for action in possible_actions:
    #         next_state = state.take_action(action)
    #         if next_state is None:
    #             continue
    #         distance = abs(next_state.robot_loc[0] - next_state.goal_loc[0]) + abs(next_state.robot_loc[1] - next_state.goal_loc[1])
    #         if distance < min_distance:
    #             min_distance = distance
    #             best_action = action
    #     return best_action if best_action else random.choice(possible_actions)
    
class MCTSGameState:
    """
    Wrapper class to integrate the labyrinth state with MCTS. 
    """

    def __init__(self, environment: Environment, robot_loc, goal_loc, reward=0, is_terminal=False):
        self.environment = environment
        self.robot_loc = robot_loc
        self.goal_loc = goal_loc
        self.reward = reward
        self.is_terminal_state = is_terminal

    # def get_possible_actions(self):
    #     possible_actions = []
    #     for axis in [Axis.ROW, Axis.COL]:
    #         for shift_index in range(self.environment.N):
    #             shift_dirs = [DIRECTION.LEFTWARDS, DIRECTION.RIGHTWARDS] if axis == Axis.ROW else [DIRECTION.UPWARDS, DIRECTION.DOWNWARDS]
    #             for shift_dir in shift_dirs:
    #                 for move_direction in [0, 1, 2, 3]:  # LEFT, RIGHT, UP, DOWN
    #                     action = (axis, shift_dir, shift_index, move_direction)
    #                     possible_actions.append(action)
    #     return possible_actions
    def get_possible_actions(self):
        # First, build the graph of cards
        card_graph = self.environment.build_card_graph()
        
        # Get the current card number of the robot
        robot_row, robot_col = self.robot_loc
        current_card_num = (robot_row // 3) * self.environment.N + (robot_col // 3)
        
        # Fetch the list of accessible cards from the current card
        accessible_cards = card_graph.get(current_card_num, [])

        possible_actions = []
        # Iterate over accessible cards and determine the direction to move
        for next_card_num in accessible_cards:
            
            
            # Determine the move direction based on the current and next card positions
            if next_card_num == current_card_num - self.environment.N:  # Moving up
                possible_actions.append(DIRECTION.UPWARDS)
            elif next_card_num == current_card_num + self.environment.N:  # Moving down
                possible_actions.append(DIRECTION.DOWNWARDS)
            elif next_card_num == current_card_num - 1:  # Moving left
                possible_actions.append(DIRECTION.LEFTWARDS)
            elif next_card_num == current_card_num + 1:  # Moving right
                possible_actions.append(DIRECTION.RIGHTWARDS)

        return possible_actions

    def get_current_card(self):
        # Assuming card numbering starts from 0 and it's a grid-based board
        robot_row, robot_col = self.robot_loc
        card_number = (robot_row // 3) * self.environment.N + (robot_col // 3)
        return card_number

    def take_action(self, action):
        new_env = copy.deepcopy(self.environment)
        # print("Action taken: ", action)
        state, reward, is_terminal = new_env.step(action)
        self.reward = reward
        self.is_terminal_state = is_terminal
        if state is None:
            # Handle illegal action
            return None
        new_robot_loc = new_env.robot_loc
        return MCTSGameState(new_env, new_robot_loc, self.goal_loc, reward, is_terminal)

    def is_terminal(self):
        return self.is_terminal_state

    def get_reward(self):
        return self.reward
    
    # def possible_moves(self):
    #     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    #     possible_moves = []
    #     for d in directions:
    #         new_x = self.robot_loc[0] + d[0]
    #         new_y = self.robot_loc[1] + d[1]
    #         if 0 <= new_x < self.environment.board.shape[0] and 0 <= new_y < self.environment.board.shape[1] and self.environment.board[new_x][new_y] != 0:
    #             possible_moves.append((self.robot_loc, (new_x, new_y)))
    #     print("Possible moves: ", possible_moves)
    #     return possible_moves
    
    # def get_possible_envs(self):
    #     possible_envs = []
    #     for i in range(self.N):
    #         for direction in DIRECTION:
    #             if self.shift_cards(axis=Axis.ROW, dir=direction, card_row_or_col=i):
    #                 possible_envs.append((Axis.ROW, direction, i))
    #                 self.shift_cards(axis=Axis.ROW, dir=self.opp_direction(direction), card_row_or_col=i)
    #             if self.shift_cards(axis=Axis.COL, dir=direction, card_row_or_col=i):
    #                 possible_envs.append((Axis.COL, direction, i))
    #                 self.shift_cards(axis=Axis.COL, dir=self.opp_direction(direction), card_row_or_col=i)
    #     return possible_envs
       
    
    # def opp_direction(self, direction):
    #     match direction:
    #         case DIRECTION.LEFTWARDS:
    #             return DIRECTION.RIGHTWARDS
    #         case DIRECTION.RIGHTWARDS:
    #             return DIRECTION.LEFTWARDS
    #         case DIRECTION.UPWARDS:
    #             return DIRECTION.DOWNWARDS
    #         case DIRECTION.DOWNWARDS:
    #             return DIRECTION.UPWARDS
    
    # def get_distance(self, loc1, loc2):
    #     return math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)


if __name__ == "__main__":

    environment = Environment(instance_file="/Users/dunliang/Downloads/cs4246-labyrinth/3x3_instances_pddl/instance_4_3_by_3.pddl")
    initial_state = MCTSGameState(environment, environment.robot_loc, (environment.N - 1, environment.N - 1))
    # agent = MCTSAgent(environment, num_simulations=500)
    
    agent = MCTSAgent(environment, num_simulations=5)

    environment.print_board_prettier()
    current_state = initial_state
    is_terminal = current_state.is_terminal()  # Start with checking if the initial state is terminal (should be False)

    actions_taken = []

    best_node = agent.search(current_state)
    # if best_node:
    #     best_action = best_node.action
    #     actions_taken.append(best_action)  # Store the action
    #     print("Best action found by MCTS: ", best_action.__str__())
    #     best_action_index = best_action[1].value

    #     # Apply the best action to the real environment
    #     state, reward, is_terminal = environment.step(best_action_index)

    #     # Update the current state after applying the action
    #     current_state = MCTSGameState(environment, environment.robot_loc, (environment.N - 1, environment.N - 1))
        
    #     # Print the board after each move
    #     environment.print_board_prettier()


    # if best_node:
    #     best_action = best_node.action
    #     actions_taken.append(best_action)
    #     print("Best action found by MCTS: ", best_action)
    #     state, reward, is_terminal = environment.step(best_action)
    #     current_state = MCTSGameState(environment, environment.robot_loc, (environment.N - 1, environment.N - 1))
    #     # environment.print_board_prettier()


    while not is_terminal:
        # Use MCTS to find the best action from the current state
        best_node = agent.search(current_state)

        if best_node:
            best_action = best_node.action
            actions_taken.append(best_action)  # Store the action
            print("Best action found by MCTS: ", best_action)

            # Apply the best action to the real environment
            state, reward, is_terminal = environment.step(best_action)

            # Update the current state after applying the action
            current_state = MCTSGameState(environment, environment.robot_loc, environment.goal_loc)
            environment.print_board_prettier() 
        else:
            print("No valid action found by MCTS.")
            break  # If no valid action is found, exit the loop

    # After exiting the loop, check if the goal was reached
    if is_terminal:
        print("Goal reached successfully!")
        print("Sequence of actions to reach the goal:")
        for idx, action in enumerate(actions_taken):
            print(f"Step {idx + 1}: {action}")
    else:
        print("Failed to reach the goal.")

    