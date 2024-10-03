from environment.Environment import Environment
import numpy as np
import random

if __name__ == "__main__":
    FILENAME = "/Users/russelltankaimin/Desktop/python_proj/project-labyrinth/3x3_instances_pddl/instance_139_3_by_3.pddl"
    env = Environment(FILENAME)
    env.print_board_prettier()
    board, reward, done = env.step(3)
    env.print_board_prettier()
    N_EPISODES = 2000
    for i in range(N_EPISODES):
        env.print_board_prettier()
        board, reward, done = env.step(random.choice([1,2,3,4]))
        env.print_board_prettier()
        if done:
            print("Terminal!")
            break
    

    print("So far ok!")