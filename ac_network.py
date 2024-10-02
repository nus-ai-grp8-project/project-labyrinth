from environment.Environment import Environment
import numpy as np

if __name__ == "__main__":
    FILENAME = "/Users/russelltankaimin/Desktop/python_proj/project-labyrinth/7x7_instances_pddl/instance_139_7_by_7.pddl"
    env = Environment(FILENAME)
    env.print_board_prettier()
    # print(env.build_card_graph())
    env.build_card_graph()
    N_EPISODES = 2000

    print("So far ok!")