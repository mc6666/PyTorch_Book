# -*- coding: utf-8 -*-
# 修改自 https://medium.com/quick-code/python-audio-spectrum-analyser-6a3c54ad950
import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# 宣告麥克風變數
mic = pyaudio.PyAudio()

# 參數設定
FORMAT = pyaudio.paInt16 # 精度
CHANNELS = 1 # 單聲道
RATE = 48000 # 取樣頻率
INTERVAL = 0.32 # 緩衝區大小
CHUNK = int(RATE * INTERVAL) # 接收區塊大小

# 開啟麥克風
stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
            input=True, output=True, frames_per_buffer=CHUNK)

i=0
while i < 100: # 顯示100次即停止
    data = stream.read(CHUNK, exception_on_overflow=False)
    data = np.frombuffer(data, dtype='b')
    
    # 繪製頻譜圖
    f, t, Sxx = signal.spectrogram(data, fs=CHUNK)
    dBS = 10 * np.log10(Sxx)
    plt.clf()
    # 設定X/Y軸標籤
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')

    plt.pcolormesh(t, f, dBS)
    plt.pause(0.001)
    i+=1

# 關閉所有裝置    
stream.stop_stream()
stream.close()
mic.terminate()


