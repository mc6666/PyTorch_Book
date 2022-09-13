# -*- coding: utf-8 -*-
# 修改自 https://medium.com/quick-code/python-audio-spectrum-analyser-6a3c54ad950
import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# 宣告麦克风变数
mic = pyaudio.PyAudio()

# 参数设定
FORMAT = pyaudio.paInt16 # 精度
CHANNELS = 1 # 单声道
RATE = 20000 # 取样频率
CHUNK = int(RATE/20) # 接收区块大小

# 开启麦克风
stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
            input=True, output=True, frames_per_buffer=CHUNK)

# +
fig, ax = plt.subplots(figsize=(14,6))

# 设定X/Y轴范围
ax.set_ylim(-200, 200)
ax.set_xlim(0, CHUNK)

# 绘图
x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))
i=0
while i < 100:
    data = stream.read(CHUNK, exception_on_overflow=False)
    data = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2]
    #data = abs(data)
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.005)
    i+=1
# -

# 关闭所有装置    
stream.stop_stream()
stream.close()
mic.terminate()



