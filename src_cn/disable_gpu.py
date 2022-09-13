# 载入套件
import torch
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# 检查 GPU 及 cuda toolkit 是否存在
print(torch.cuda.is_available())