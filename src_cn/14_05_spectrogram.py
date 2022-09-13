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
RATE = 48000 # 取样频率
INTERVAL = 0.32 # 缓冲区大小
CHUNK = int(RATE * INTERVAL) # 接收区块大小

# 开启麦克风
stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
            input=True, output=True, frames_per_buffer=CHUNK)

i=0
while i < 100: # 显示100次即停止
    data = stream.read(CHUNK, exception_on_overflow=False)
    data = np.frombuffer(data, dtype='b')
    
    # 绘制频谱图
    f, t, Sxx = signal.spectrogram(data, fs=CHUNK)
    dBS = 10 * np.log10(Sxx)
    plt.clf()
    # 设定X/Y轴标签
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')

    plt.pcolormesh(t, f, dBS)
    plt.pause(0.001)
    i+=1

# 关闭所有装置    
stream.stop_stream()
stream.close()
mic.terminate()


