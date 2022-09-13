# streamlit run 05_07_web.py
# 载入套件
import streamlit as st 
from skimage import io
from skimage.transform import resize
import numpy as np  
import torch

# 模型载入
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
@st.cache(allow_output_mutation=True)
def load_model():
    return torch.load('./model.pt').to(device)

model = load_model()

# 标题
st.title("上传图片(0~9)辨识")

# 上传图档
uploaded_file = st.file_uploader("上传图片(.png)", type="png")
if uploaded_file is not None:
    # 读取上传图档
    image1 = io.imread(uploaded_file, as_gray=True)

    # 缩为 (28, 28) 大小的影像
    image_resized = resize(image1, (28, 28), anti_aliasing=True)    
    X1 = image_resized.reshape(1,28, 28) #/ 255.0

    # 反转颜色，颜色0为白色，与 RGB 色码不同，它的 0 为黑色
    X1 = torch.FloatTensor(1-X1).to(device)

    # 预测
    predictions = torch.softmax(model(X1), dim=1)

    # 显示预测结果
    st.write(f'### 预测结果:{np.argmax(predictions.detach().cpu().numpy())}')

    # 显示上传图档
    st.image(image1)
