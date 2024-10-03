import sys
import torch 
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from environment.Environment import Environment


# hyperparameters
hidden_size = 256
learning_rate = 3e-4

# Constants
GAMMA = 0.95
num_steps = 1300
max_episodes = 5000

class ActorCritic(nn.Module):
    def __init__(self, num_inputs, num_actions, hidden_size, learning_rate=3e-4):
        super(ActorCritic, self).__init__()

        self.num_actions = num_actions
        self.critic_linear1 = nn.Linear(num_inputs, hidden_size)
        self.critic_linear2 = nn.Linear(hidden_size, 1)

        self.actor_linear1 = nn.Linear(num_inputs, hidden_size)
        self.actor_linear2 = nn.Linear(hidden_size, num_actions)
    
    def forward(self, state):
        state = Variable(torch.from_numpy(state).float().unsqueeze(0))
        value = F.relu(self.critic_linear1(state))
        value = self.critic_linear2(value)
        
        policy_dist = F.relu(self.actor_linear1(state))
        policy_dist = F.softmax(self.actor_linear2(policy_dist), dim=1)

        return value, policy_dist
    
def advantage_actor_critic(env, plot=False):
    num_inputs = env.N * env.N * 3 * 3
    num_outputs = 4

    min_steps = 1000000
    best_model = None
    
    actor_critic = ActorCritic(num_inputs, num_outputs, hidden_size)
    ac_optimizer = optim.Adam(actor_critic.parameters(), lr=learning_rate)

    all_lengths = []
    average_lengths = []
    all_rewards = []
    entropy_term = 0

    for episode in range(max_episodes):
        log_probs = []
        values = []
        rewards = []

        state = env.reset()

        #print(f"state : {state}")
        for steps in range(num_steps):
            value, policy_dist = actor_critic.forward(state)
            value = value.detach().numpy()[0,0]
            dist = policy_dist.detach().numpy() 

            action = np.random.choice(num_outputs, p=np.squeeze(dist))
            log_prob = torch.log(policy_dist.squeeze(0)[action])
            entropy = -np.sum(np.mean(dist) * np.log(dist))
            new_state, reward, done = env.step(action + 1)

            rewards.append(reward)
            values.append(value)
            log_probs.append(log_prob)
            entropy_term += entropy
            state = new_state
            
            if done or steps == num_steps-1:
                Qval, _ = actor_critic.forward(new_state)
                Qval = Qval.detach().numpy()[0,0]
                all_rewards.append(np.sum(rewards))
                all_lengths.append(steps)
                average_lengths.append(np.mean(all_lengths[-10:]))
                if episode % 10 == 0:                    
                    sys.stdout.write("episode: {}, reward: {}, total length: {}, average length: {} dist : {}\n".format(episode, np.sum(rewards), steps, average_lengths[-1], np.squeeze(dist)))
                break
        
        # compute Q values
        Qvals = np.zeros_like(values)
        for t in reversed(range(len(rewards))):
            Qval = rewards[t] + GAMMA * Qval
            Qvals[t] = Qval
  
        #update actor critic
        values = torch.FloatTensor(values)
        Qvals = torch.FloatTensor(Qvals)
        log_probs = torch.stack(log_probs)
        
        advantage = Qvals - values
        actor_loss = (-log_probs * advantage).mean()
        critic_loss = 0.5 * advantage.pow(2).mean()
        ac_loss = actor_loss + critic_loss + 0.001 * entropy_term

        ac_optimizer.zero_grad()
        ac_loss.backward()
        ac_optimizer.step()

        
    if plot:
        # Plot results
        smoothed_rewards = pd.Series.rolling(pd.Series(all_rewards), 10).mean()
        smoothed_rewards = [elem for elem in smoothed_rewards]
        # plt.plot(all_rewards)
        plt.plot(smoothed_rewards)
        plt.plot()
        plt.xlabel('Episode')
        plt.ylabel('Reward')
        plt.show()

        # plt.plot(all_lengths)
        plt.plot(average_lengths)
        plt.xlabel('Episode')
        plt.ylabel('Episode length')
        plt.show()
    return actor_critic

if __name__ == "__main__":
    FILENAME = "/Users/russelltankaimin/Desktop/python_proj/project-labyrinth/3x3_instances_pddl/instance_139_3_by_3.pddl"
    env = Environment(FILENAME)
    model = advantage_actor_critic(env, plot=True)

    test_env = Environment(FILENAME)
    state = np.array(test_env.board)
    state = state.flatten()

    done = False
    steps = 0
    while not done:
        _, policy_dist = model.forward(state)
        policy_dist = policy_dist.detach().numpy() 
        action = np.random.choice(4, p=np.squeeze(policy_dist))
        state, reward, done = test_env.step(action + 1)
        steps += 1
    
    print(f"Model solved in {steps} steps!")

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