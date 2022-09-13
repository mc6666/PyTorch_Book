import pyaudio
import sys
from array import array
from sys import byteorder
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000 #44100

# 录音长度
RECORD_SECONDS = 2

if len(sys.argv) < 2:
    file_path = './demo.wav'
else:
    file_path = sys.argv[1]

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS, 
                rate=RATE, 
                input=True,
                output=True,
                frames_per_buffer=CHUNK)
wf = wave.open(file_path, 'wb')
wf.setnchannels(CHANNELS)
# sample_width: 2 ==> 16 bits, 1 ==> 8 bits
sample_width = p.get_sample_size(FORMAT)
wf.setsampwidth(sample_width)
wf.setframerate(RATE)
print ("start recording")

# https://docs.python.org/zh-tw/3/library/array.html
# signed short
data_all=[]
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    #print(type(data))
    #print(len(data))
    wf.writeframes(data)
    data_all += data_all
print ("end recording")
