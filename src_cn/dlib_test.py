# 载入相关套件
import dlib
import cv2
import numpy as np
from matplotlib import pyplot as plt

# 载入模型
pose_predictor_5_point = dlib.shape_predictor("./OpenCV/shape_predictor_5_face_landmarks.dat")
face_encoder = dlib.face_recognition_model_v1("./OpenCV/dlib_face_recognition_resnet_model_v1.dat")
detector = dlib.get_frontal_face_detector()

# 找出哪一张脸最相似
def compare_faces_ordered(encodings, face_names, encoding_to_check):
    distances = list(np.linalg.norm(encodings - encoding_to_check, axis=1))
    return zip(*sorted(zip(distances, face_names)))


# 利用线性代数的法向量比较两张脸的特征点
def compare_faces(encodings, encoding_to_check):
    return list(np.linalg.norm(encodings - encoding_to_check, axis=1))

# 图像编码
def face_encodings(face_image, number_of_times_to_upsample=1, num_jitters=1):
    # 侦测脸部
    face_locations = detector(face_image, number_of_times_to_upsample)
    # 侦测脸部特征点
    raw_landmarks = [pose_predictor_5_point(face_image, face_location) 
                     for face_location in face_locations]
    # 编码
    return [np.array(face_encoder.compute_face_descriptor(face_image, 
                                    raw_landmark_set, num_jitters)) for
                                    raw_landmark_set in raw_landmarks]
                                    
# 载入图档
known_image_1 = cv2.imread("./images_face/jared_1.jpg")
known_image_2 = cv2.imread("./images_face/jared_2.jpg")
known_image_3 = cv2.imread("./images_face/jared_3.jpg")
known_image_4 = cv2.imread("./images_face/obama.jpg")
unknown_image = cv2.imread("./images_face/jared_4.jpg")
names = ["jared_1.jpg", "jared_2.jpg", "jared_3.jpg", "obama.jpg"]

# 图像编码
known_image_1_encoding = face_encodings(known_image_1)[0]
known_image_2_encoding = face_encodings(known_image_2)[0]
known_image_3_encoding = face_encodings(known_image_3)[0]
known_image_4_encoding = face_encodings(known_image_4)[0]
known_encodings = [known_image_1_encoding, known_image_2_encoding, 
                   known_image_3_encoding, known_image_4_encoding]
unknown_encoding = face_encodings(unknown_image)[0]

# 比对
computed_distances = compare_faces(known_encodings, unknown_encoding)
computed_distances_ordered, ordered_names = compare_faces_ordered(known_encodings, 
                                                      names, unknown_encoding)
print('比较两张脸的法向量距离：', computed_distances)
print('排序：', computed_distances_ordered)
print('依相似度排序：', ordered_names)                                    