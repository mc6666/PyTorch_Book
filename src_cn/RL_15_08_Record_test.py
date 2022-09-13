# ffmpeg.exe 放在Path的路径下  
# mac: brew install ffmpeg
# 载入相关套件
import gym

# 载入环境
env = gym.make("CartPole-v0")

# 录影
env = gym.wrappers.Monitor(env, "recording", force=True)

# 实验
for _ in range(50):
    total_reward = 0.0
    obs = env.reset()

    while True:
        env.render()
        action = env.action_space.sample()
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            break

    print(f"报酬: {total_reward:.2f}")
    
env.close()
