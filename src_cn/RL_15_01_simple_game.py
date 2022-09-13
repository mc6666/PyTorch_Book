# 载入相关套件
import random

# 环境类别
class Environment:    
    def __init__(self): # 初始化       
        self.poistion = 3 # 玩家一开始站中间位置

    def get_observation(self):
        # 状态空间(State Space)，共有5个位置
        return [i for i in range(1, 6)]

    def get_actions(self):        
        return [-1, 1] # 行动空间(Action Space)

    def is_done(self): # 判断比赛回合是否结束
        # 是否走到左右端点
        return self.poistion == 1 or self.poistion == 5

    # 步骤
    def step(self, action):
        # 是否回合已结束
        if self.is_done():
            raise Exception("Game over")
        
        self.poistion += action
        if self.poistion == 1:
            reward = -1
        elif self.poistion == 5:
            reward = 1
        else:    
            reward = -0.02

        return self.poistion, reward


# 代理人类别
class Agent:
    # 初始化
    def __init__(self):
        pass
        
    def action(self, env):
        # 取得状态
        current_obs = env.get_observation()
        # 随机行动
        return random.choice(env.get_actions())


if __name__ == "__main__":
    # 建立实验，含环境、代理人物件
    env = Environment()
    agent = Agent()

    # 进行实验
    total_reward=0  # 累计报酬
    action_list = []
    while not env.is_done():
        # 采取行动
        action = agent.action(env)
        action_list += [action]
        
        # 更新下一步
        state, reward = env.step(action)
        
        # 计算累计报酬
        total_reward += reward
    
    # 显示累计报酬
    print(f"累计报酬: {total_reward:.4f}")
    print(f"行动: {action_list}")

