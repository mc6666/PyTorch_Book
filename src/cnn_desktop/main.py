from tkinter import *
from tkinter import filedialog
from PIL import ImageDraw, Image, ImageGrab
import numpy as np
from skimage import color
from skimage import io
import os
import io
import torch
import torch
from torch import nn
from torch.nn import functional as F

class Paint(object):

    # 類別初始化函數
    def __init__(self):
        self.root = Tk()
        
        self.root.title('手寫阿拉伯數字辨識')

        #defining Canvas
        self.c = Canvas(self.root, bg='white', width=280, height=280)
        
        self.image1 = Image.new('RGB', (280, 280), color = 'white')
        self.draw = ImageDraw.Draw(self.image1) 

        self.c.grid(row=1, columnspan=6)

        # 建立【辨識】按鈕
        self.classify_button = Button(self.root, text='辨識', command=lambda:self.classify(self.c))
        self.classify_button.grid(row=0, column=0, columnspan=2, sticky='EWNS')

        # 建立【清畫面】按鈕
        self.clear = Button(self.root, text='清畫面', command=self.clear)
        self.clear.grid(row=0, column=2, columnspan=2, sticky='EWNS')

        # 建立【存檔】按鈕
        self.savefile = Button(self.root, text='存檔', command=self.savefile)
        self.savefile.grid(row=0, column=4, columnspan=2, sticky='EWNS')

        # 建立【預測】文字框
        self.prediction_text = Text(self.root, height=2, width=10)
        self.prediction_text.grid(row=2, column=4, columnspan=2)

        # self.model = self.loadModel()
        
        # 定義滑鼠事件處理函數
        self.setup()
        
        # 監聽事件
        self.root.mainloop()

    # 滑鼠事件處理函數
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 15
        self.color = 'black'
        
        # 定義滑鼠事件處理函數，包括移動滑鼠及鬆開滑鼠按鈕
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    # 移動滑鼠 處理函數
    def paint(self, event):
        paint_color = self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            # 顯示設定>100%，抓到的區域會變小
            # 畫圖同時寫到記憶體，避免螢幕字型放大，造成抓到的畫布區域不足
            self.draw.line((self.old_x, self.old_y, event.x, event.y), fill='black', width=self.line_width)

        self.old_x = event.x
        self.old_y = event.y

    # 鬆開滑鼠按鈕 處理函數
    def reset(self, event):
        self.old_x, self.old_y = None, None

    # 【清畫面】處理函數
    def clear(self):
        self.c.delete("all")
        self.image1 = Image.new('RGB', (280, 280), color = 'white')
        self.draw = ImageDraw.Draw(self.image1) 
        self.prediction_text.delete("1.0", END)

    # 【存檔】處理函數
    def savefile(self):
        f = filedialog.asksaveasfilename( defaultextension=".png", filetypes = [("png file",".png")])
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        #print(f)
        self.image1.save(f)

    # 【辨識】處理函數
    def classify(self, widget):
        # self.image1.save('原圖.png')
        img = self.image1.resize((28, 28), ImageGrab.Image.ANTIALIAS).convert('L')
        # img.save('縮小.png')
        
        img = np.array(img)
        # Change pixels to work with our classifier
        img = (255 - img) / 255
        
        img2=Image.fromarray(img) 
        #img2.save('2.png')

        # 圖像轉為 PyTorch 張量
        img = np.reshape(img, (1, 1, 28, 28))
        data = torch.FloatTensor(img).to(device)
        
        # 預測
        output = model(data)
        # Get index with highest probability
        _, predicted = torch.max(output.data, 1)
        #print(pred)
        self.prediction_text.delete("1.0", END)
        self.prediction_text.insert(END, predicted.item())

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output

# 載入模型
def loadModel():    
    model = torch.load('cnn_augmentation_model.pt').to(device)
    return model
        
if __name__ == '__main__':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("cuda" if torch.cuda.is_available() else "cpu")

    # 載入既有的模型
    print('load model ...')
    model = loadModel()
    
    # 顯示視窗
    Paint()

