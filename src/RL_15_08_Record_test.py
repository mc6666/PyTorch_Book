# ffmpeg.exe 放在Path的路徑下  
# mac: brew install ffmpeg
# 載入相關套件
import gym

# 載入環境
env = gym.make("CartPole-v0")

# 錄影
env = gym.wrappers.Monitor(env, "recording", force=True)

# 實驗
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

    print(f"報酬: {total_reward:.2f}")
    
env.close()
