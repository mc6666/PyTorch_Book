# 載入相關套件
import random

# 環境類別
class Environment:    
    def __init__(self): # 初始化       
        self.poistion = 3 # 玩家一開始站中間位置

    def get_observation(self):
        # 狀態空間(State Space)，共有5個位置
        return [i for i in range(1, 6)]

    def get_actions(self):        
        return [-1, 1] # 行動空間(Action Space)

    def is_done(self): # 判斷比賽回合是否結束
        # 是否走到左右端點
        return self.poistion == 1 or self.poistion == 5

    # 步驟
    def step(self, action):
        # 是否回合已結束
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


# 代理人類別
class Agent:
    # 初始化
    def __init__(self):
        pass
        
    def action(self, env):
        # 取得狀態
        current_obs = env.get_observation()
        # 隨機行動
        return random.choice(env.get_actions())


if __name__ == "__main__":
    # 建立實驗，含環境、代理人物件
    env = Environment()
    agent = Agent()

    # 進行實驗
    total_reward=0  # 累計報酬
    action_list = []
    while not env.is_done():
        # 採取行動
        action = agent.action(env)
        action_list += [action]
        
        # 更新下一步
        state, reward = env.step(action)
        
        # 計算累計報酬
        total_reward += reward
    
    # 顯示累計報酬
    print(f"累計報酬: {total_reward:.4f}")
    print(f"行動: {action_list}")

