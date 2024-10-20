import random
from environment.Environment import Environment, Axis, DIRECTION
import numpy as np
import math
import copy
import os

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

    

    
    def best_child(self, exploration_weight=1.4):
        if len(self.children) == 0:
            while len(self.state.get_possible_actions()) == 0:
                self.state.environment.shift_board(TO_SHIFT=1)
            self.state.environment.update_goal_location()

            possible_actions = self.state.get_possible_actions()
            for action in possible_actions:
                next_state = self.state.take_action(action)
                child_node = MCTSNode(state=next_state, parent=self)
                self.children.append(child_node)
            # raise ValueError("No children found to select the best child from.")
        
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
            if not choices_weights:
                return None  # or handle accordingly


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
        # print(f"Backpropagating - Node reward: {self.reward}, Visits: {self.visits}, Current State: {current_card_number}")
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
            # Ensure the node has children before attempting to select the best one
                if len(node.children) == 0:
                    return node  # Stop here if no children are available, to avoid raising an error
                node = node.get_best_child()
        return node
    


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

    # def take_action(self, action):
    #     new_env = copy.deepcopy(self.environment)
    #     # print("Action taken: ", action)
    #     state, reward, is_terminal = new_env.step(action)
    #     self.reward = reward
    #     self.is_terminal_state = is_terminal
    #     if state is None:
    #         # Handle illegal action
    #         return None
    #     new_robot_loc = new_env.robot_loc
    #     return MCTSGameState(new_env, new_robot_loc, self.goal_loc, reward, is_terminal)
    def take_action(self, action):
        new_env = copy.deepcopy(self.environment)

        # Perform a random card shift before taking action
        TO_SHIFT = 1
        shifted = 0
        while shifted < TO_SHIFT:
            random_axis = random.choice([Axis.ROW, Axis.COL])
            random_idx = random.choice([i for i in range(new_env.N)])
            random_dir = random.choice([DIRECTION.LEFTWARDS, DIRECTION.RIGHTWARDS] if random_axis == Axis.ROW else [DIRECTION.UPWARDS, DIRECTION.DOWNWARDS])
            if new_env.shift_cards(axis=random_axis, dir=random_dir, card_row_or_col=random_idx):
                shifted += 1
        new_env.update_goal_location()

        # Take the robot movement action
        state, reward, is_terminal = new_env.step(action)
        if state is None:
            # Handle illegal action
            return None
        new_robot_loc = new_env.robot_loc

        return MCTSGameState(new_env, new_robot_loc, new_env.goal_loc, reward, is_terminal)


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
    
    
    # environment = Environment(instance_file="/Users/dunliang/Downloads/cs4246-labyrinth/3x3_instances_pddl/instance_3_3_by_3.pddl")
    # initial_state = MCTSGameState(environment, environment.robot_loc, (environment.N - 1, environment.N - 1))
    # # agent = MCTSAgent(environment, num_simulations=500)
    
    # agent = MCTSAgent(environment, num_simulations=10)

    # environment.print_board_prettier()
    # current_state = initial_state
    # is_terminal = current_state.is_terminal()  # Start with checking if the initial state is terminal (should be False)

    # actions_taken = []

    # best_node = agent.search(current_state)

    # while not is_terminal:
    #     # Use MCTS to find the best action from the current state
    #     best_node = agent.search(current_state)

    #     if best_node:
    #         best_action = best_node.action
    #         actions_taken.append(best_action)  # Store the action
    #         print("Best action found by MCTS: ", best_action)

    #         # Apply the best action to the real environment
    #         state, reward, is_terminal = environment.step(best_action)

    #         # Update the current state after applying the action
    #         current_state = MCTSGameState(environment, environment.robot_loc, environment.goal_loc)
    #         environment.print_board_prettier() 
    #     else:
    #         print("No valid action found by MCTS.")
    #         break  # If no valid action is found, exit the loop

    # # After exiting the loop, check if the goal was reached
    # if is_terminal:
    #     print("Goal reached successfully!")
    #     print("Sequence of actions to reach the goal:")
    #     for idx, action in enumerate(actions_taken):
    #         print(f"Step {idx + 1}: {action}")
    # else:
    #     print("Failed to reach the goal.")

    
## Can try to run the same maze multiple times and use the average of the steps required to 
# reach the goal as a metric to compare the performance of the MCTS agent with the random agent.



    # Path to the folder containing all 3x3 maze instances
    instances_path = "/Users/dunliang/Downloads/cs4246-labyrinth/7x7_instances_pddl/"

    # Number of times to test all the mazes
    NUM_TESTS = 10
    STARTING_INSTANCE = 0
    ENDING_INSTANCE = 1

    
    # Create or open the results file for writing
    with open("7x7_result.txt", "a") as result_file:
        # Iterate over all the instance files in the directory
        result_file.write(f"Results for instances {STARTING_INSTANCE} to {ENDING_INSTANCE}:\n")
        for instance_num in range(STARTING_INSTANCE, ENDING_INSTANCE + 1):  # Assuming instances are from 0 to 249
            instance_file = os.path.join(instances_path, f"instance_{instance_num}_7_by_7.pddl")
            print(f"Testing instance: {instance_file}")
            
            # List to store steps taken for each test run for this instance
            steps_taken_list = []

            # Iterate over the number of tests
            for test_run in range(1, NUM_TESTS + 1):
                # Initialize the environment and the initial state
                environment = Environment(instance_file=instance_file)
                initial_state = MCTSGameState(environment, environment.robot_loc, (environment.N - 1, environment.N - 1))
                agent = MCTSAgent(environment, num_simulations=10)

                # Set up the initial conditions
                current_state = initial_state
                is_terminal = current_state.is_terminal()
                actions_taken = []

                # Run MCTS until the goal is reached or no valid action is found
                while not is_terminal:
                    best_node = agent.search(current_state)

                    if best_node:
                        best_action = best_node.action
                        actions_taken.append(best_action)

                        # Apply the best action to the real environment
                        state, reward, is_terminal = environment.step(best_action)

                        # Update the current state after applying the action
                        current_state = MCTSGameState(environment, environment.robot_loc, environment.goal_loc)
                    else:
                        break

                # Record the number of steps taken for this test run
                steps_taken_list.append(len(actions_taken))

                # # Record the result for this instance and test run
                # if is_terminal:
                #     result_file.write(f"Instance {instance_num}, Test Run {test_run}: Goal reached in {len(actions_taken)} steps.\n")
                # else:
                #     result_file.write(f"Instance {instance_num}, Test Run {test_run}: Failed to reach the goal.\n")
            

            # Calculate the average steps taken for this instance across all test runs
            if steps_taken_list:
                average_steps = sum(steps_taken_list) / len(steps_taken_list)
                # result_file.write(f"Instance {instance_num}: Average steps taken across {NUM_TESTS} test runs: {average_steps:.2f}\n")
                result_file.write(f"{average_steps:.2f}")
            else:
                result_file.write(f"Instance {instance_num}: No valid runs were completed.\n")

            # Separate instances in the result file for readability
            result_file.write("\n")

    print("All instances have been tested and results are recorded in '7x7_result.txt'.")