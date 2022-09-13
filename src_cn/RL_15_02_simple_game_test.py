# 载入相关套件
from RL_15_01_simple_game import Environment, Agent

# 建立实验，含环境、代理人物件
env = Environment()
agent = Agent()

# 进行实验
for _ in range(10):
    env.__init__()  # 重置
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
