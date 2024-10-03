import sys
import pandas as pd
import random
import numpy as np
from environment.Environment import Environment, DIRECTION, Axis

maps = {
    (0, 1): "RIGHT",
    (0, -1): "LEFT",
    (1, 0) : "DOWN",
    (-1, 0): "UP"
}
def random_player(env):

    def feasible(board, x, y, x_lim, y_lim):
        return 0 <= x <= x_lim and 0 <= y <= y_lim and board[x, y] != 0
    
    board = env.board
    steps = 0
    x_limit = 3 * env.N - 1
    y_limit = 3 * env.N - 1
    done = False
    while not done:
        TO_SHIFT = 1
        shifted = 0
        while shifted < TO_SHIFT:
            # pick row or col to shift
            random_axis = random.choice([Axis.ROW, Axis.COL]) # 0 for ROW, 1 for COL
            random_idx = random.choice([i for i in range(env.N)]) # Row or col index of card
            random_dir = random.choice([DIRECTION.LEFTWARDS, DIRECTION.RIGHTWARDS] if random_axis == Axis.ROW else [DIRECTION.UPWARDS, DIRECTION.DOWNWARDS]) # 2 for left (up) 3 for right (down)
            if env.shift_cards(axis=random_axis, dir=random_dir, card_row_or_col=random_idx):
                shifted += 1
                # print("Shifted!")
        x_r, y_r = env.robot_loc
        dir = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        n_x = x_r + dir[0]
        n_y = y_r + dir[1]
        while (not feasible(env.board, n_x, n_y, x_limit, y_limit)):
            dir = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
            n_x = x_r + dir[0]
            n_y = y_r + dir[1]
        env.robot_loc = (n_x, n_y)
        # print(f"Move : {maps[(n_x - x_r, n_y - y_r)]}")
        env.board[x_r, y_r] = 1
        if env.board[n_x, n_y] == 5:
            break
        env.board[n_x, n_y] = 2
        # env.print_board_prettier()
        steps += 1
    # env.print_board_prettier()
    return steps


if __name__ == "__main__":
    for i in range(150):
        total_steps = 0
        for j in range(10):
            FILENAME = f"/Users/russelltankaimin/Desktop/python_proj/project-labyrinth/7x7_instances_pddl/instance_{i}_7_by_7.pddl"
            env = Environment(FILENAME)
            steps_iter = random_player(env)
            total_steps += steps_iter
        print(f"Instance {i} done in avg {total_steps / 10} steps")
    sys.exit(0)
    

    # env.print_board_prettier()
    # board, reward, done = env.step(3)
    # env.print_board_prettier()
    # N_EPISODES = 2000
    # for i in range(N_EPISODES):
    #     env.print_board_prettier()
    #     board, reward, done = env.step(random.choice([1,2,3,4]))
    #     env.print_board_prettier()
    #     if done:
    #         print("Terminal!")
    #         break
    

    print("So far ok!")