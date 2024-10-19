import pygambit as gbt
import sys
from environment.EnvironmentNash import NashEnvironment, DIRECTION, Axis

i = 1

FILENAME = f"/Users/russelltankaimin/Desktop/python_proj/project-labyrinth/3x3_instances_pddl/instance_{i}_3_by_3.pddl"

environment = NashEnvironment(FILENAME)

is_terminal = False
is_env_turn = True

mapping = {
    "D1" : 0,
    "D2" : 1,
    "U1" : 2,
    "U2" : 3,
    "L1" : 4,
    "L2" : 5,
    "R1" : 6,
    "R2" : 7,
    "L" : 0,
    "R" : 1,
    "D" : 2,
    "U" : 3
}

while not is_terminal:
    # Get possible moves from environment
    possible_moves = environment.get_possible_moves(is_env=is_env_turn)

    print(possible_moves)
    
    # obtain payoff matrix
    payoff_dict = environment.get_payoff_map(possible_moves=possible_moves, is_env_turn=is_env_turn)
    print(f"Number of valid move combinations out of 32 : {len(payoff_dict)}")
    # build game tree
    game = gbt.Game.new_table([4, 8], title=f"3 x 3 Labyrinth Game Instance {i}")
    for payoff_, val in payoff_dict.items():
        row_player = payoff_[0]
        col_player = payoff_[1]
        game[mapping[row_player], mapping[col_player]][game.players[0]] = val[0]
        game[mapping[row_player], mapping[col_player]][game.players[1]] = val[1]

    soln = gbt.nash.enummixed_solve(game)
    for equil in soln.equilibria:
        equil = list(equil)
        print(equil)

        sys.exit(0)


    # find Pure/Mixed Strategy Nash Equilibrium

    # Extract Action

    # Execute action
    is_env_turn = not is_env_turn
