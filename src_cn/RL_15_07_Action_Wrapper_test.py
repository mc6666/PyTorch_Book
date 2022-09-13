# 载入相关套件
import gym
import random

# 继承 gym.ActionWrapper 基础类别
class RandomActionWrapper(gym.ActionWrapper):
    def __init__(self, env, epsilon=0.1):
        super(RandomActionWrapper, self).__init__(env)
        self.epsilon = epsilon # 随机行动的机率

    def action(self, action):
        # 随机乱数小于 epsilon，采取随机行动
        if random.random() < self.epsilon:
            print("Random!")
            return self.env.action_space.sample()
        return action


if __name__ == "__main__":
    env = RandomActionWrapper(gym.make("CartPole-v0"))

    for _ in range(50):
        env.reset()
        total_reward = 0.0
        while True:
            env.render()
            # 固定往左走
            print("往左走!")
            obs, reward, done, _ = env.step(0)
            total_reward += reward
            if done:
                break

        print(f"报酬: {total_reward:.2f}")
    env.close()
