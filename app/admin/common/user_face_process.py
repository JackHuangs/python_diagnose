#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2020/3/15 17:55
# @Author  : huang
# @Email   : 826652961@qq.com
# @File    : user_face_process.py
# @Software: PyCharm
# 导入open_cv-python
import cv2 as cv
import os
from app.admin.common.utils import file_rename
import numpy as np

PROCESSED_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_URL = os.path.join(PROCESSED_FILE, 'images/processed')
DETECTOR_URL = os.path.join(PROCESSED_FILE, 'lib')
STATIC_URL = "http://127.0.0.1:5000/static/processed/"


def save_face_file(file_src, types=None):
    new_pto_name = file_rename(types + ".jpg", types)
    pto_name = '{}/{}'.format(PROCESSED_URL, new_pto_name)
    cv.imwrite(pto_name, file_src)
    return new_pto_name


def face_processed(processor, scale_factor, min_neighbors, types=None, src=None, gray=None, faces=None):
    eye_num = 0
    while 1:
        organs = processor.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)
        data = np.array(organs)
        if data.size != 0:
            if types == "eyes" and data.size == 8:
                break
            elif types != "eyes" and data.size == 4:
                break
            else:
                min_neighbors = min_neighbors + 1
                if min_neighbors > 30:
                    break
        else:
            scale_factor = scale_factor + 0.01
            if scale_factor > 5:
                break
    for (x, y, w, h) in organs:
        organ_dst = src[y - 10: y + h + 10, x - 10: x + w + 10]
        # cv.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 1)
        if types == "eyes":
            if eye_num == 0:
                new_face_name = save_face_file(organ_dst, "left_eye")
                faces["left_eye"] = STATIC_URL + new_face_name
            else:
                new_face_name = save_face_file(organ_dst, "right_eye")
                faces["right_eye"] = STATIC_URL + new_face_name
            eye_num += 1
        else:
            new_face_name = save_face_file(organ_dst, types)
            faces[types] = STATIC_URL + new_face_name


# 分割人脸函数
def face_detect_demo(file_src):
    organs = {'face': None, 'left_eye': None, 'right_eye': None, 'mouth': None, 'tongue': None, 'nose': None}
    # 导入人脸级联分类器引擎
    face_detector = cv.CascadeClassifier(DETECTOR_URL + "/haarcascade_frontalface_default.xml")
    eye_detector = cv.CascadeClassifier(DETECTOR_URL + "/haarcascade_eye.xml")
    nose_detector = cv.CascadeClassifier(DETECTOR_URL + "/haarcascade_mcs_nose.xml")
    tongue_detector = cv.CascadeClassifier(DETECTOR_URL + "/haarcascade_tongue.xml")
    organs = organs

    src = cv.imread(file_src, 1)
    gray = cv.cvtColor(src, cv.COLOR_RGB2GRAY)

    face_processed(face_detector, 1.5, 3, "face", src, gray, organs)
    if organs["face"] is not None:
        face_processed(eye_detector, 1.20, 3, "eyes", src, gray, organs)
        face_processed(nose_detector, 1.20, 3, "nose", src, gray, organs)
        face_processed(tongue_detector, 1.01, 3, "tongue", src, gray, organs)
    # cv.imshow("result", src)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return organs
