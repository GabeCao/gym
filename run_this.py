import gym
from RL_brain import DeepQNetwork

def run_maze(env):
    step = 0
    times = 0
    for episode in range(9000):
        # initial observation
        print('traning times = ', times)
        times += 1
        observation = env.reset()

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done, info = env.step(action)

            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

    # end of game
    print('game over')



if __name__ == "__main__":
    # maze game
    cartPole = gym.make('Acrobot-v1')
    RL = DeepQNetwork(3, 6,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    run_maze(env=cartPole)
    RL.plot_cost()