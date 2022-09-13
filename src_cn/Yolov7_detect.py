#!/usr/bin/env python
# coding: utf-8

# python Yolov7_detect.py test.mp4 cpu

# In[1]:


import time
from pathlib import Path
import cv2
import sys
import torch
import torch.backends.cudnn as cudnn
from numpy import random
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, \
    apply_classifier, scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel


# In[2]:


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if len(sys.argv) > 2:
    device = torch.device(sys.argv[2])

# In[3]:


# Load model
weights = 'yolov7.pt'
model = attempt_load(weights, map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride

half = device.type != 'cpu'  # half precision only supported on CUDA
if half:
    model.half()  # to FP16


# In[4]:


def detect(source, img_size=640, conf_thres=0.25, save_img=False):
    dataset = LoadImages(source, img_size=img_size)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, img_size, img_size).to(device).type_as(
            next(model.parameters())))  # run once
    old_img_w = old_img_h = img_size
    old_img_b = 1

    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        print()
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img)[0]
        t2 = time_synchronized()

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres)
        t3 = time_synchronized()

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    # Add bbox to image
                    label = f'{names[int(cls)]} {conf:.2f}'
                    plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)
                    if not source.endswith('mp4'): 
                        print(label)

            cv2.imshow(str(p), im0)
            if source.endswith('mp4'):
                cv2.waitKey(1)
            else:
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
    if source.endswith('mp4'):
        cv2.destroyAllWindows()
        
    # Print time (inference + NMS)
    print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')
    print(f'Done. ({time.time() - t0:.3f}s)')
    return


# In[6]:

input_file = './test.mp4'
if len(sys.argv) > 1:
    input_file = sys.argv[1]
# detect('./inference/images/horses.jpg')
detect(input_file)


# In[ ]:




